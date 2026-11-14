"""Confirm bZIP-domain hits for candidate proteins with the EBI HMMER Pfam API."""

from __future__ import annotations

import argparse
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import pandas as pd
from Bio import SeqIO


API_BASE = "https://www.ebi.ac.uk/Tools/hmmer/api/v1"
BZIP_ACCESSIONS = {"PF00170", "PF07716", "PF03131", "PF12498"}


def request_json(url: str, data: dict | None = None) -> dict:
    payload = json.dumps(data).encode() if data is not None else None
    headers = {"User-Agent": "agri-cv-lab-bzip-reproduction/1.0"}
    if payload is not None:
        headers["Content-Type"] = "application/json"
    request = Request(url, data=payload, headers=headers)
    with urlopen(request, timeout=90) as response:
        return json.load(response)


def scan_record(record) -> dict[str, object]:
    payload = {"input": f">{record.id}\n{record.seq}\n", "database": "pfam", "E": 1.0, "domE": 1.0}
    for attempt in range(3):
        try:
            job_id = request_json(f"{API_BASE}/search/hmmscan", payload)["id"]
            for _ in range(60):
                job = request_json(f"{API_BASE}/search/{job_id}")
                status = job["task"]["status"]
                if status == "SUCCESS":
                    result = request_json(f"{API_BASE}/result/{job_id}")["result"]
                    accessions = []
                    for hit in result.get("hits", []):
                        accession = hit.get("metadata", {}).get("accession", "").split(".")[0]
                        if accession in BZIP_ACCESSIONS:
                            accessions.append(accession)
                    return {
                        "protein_fasta_id": record.id,
                        "status": "success",
                        "bzip_domain_hits": ";".join(sorted(set(accessions))),
                        "has_bzip_domain": bool(accessions),
                        "job_id": job_id,
                    }
                if status in {"ERROR", "FAILURE"}:
                    return {"protein_fasta_id": record.id, "status": status.lower(), "bzip_domain_hits": "", "has_bzip_domain": False, "job_id": job_id}
                time.sleep(2)
            return {"protein_fasta_id": record.id, "status": "timeout", "bzip_domain_hits": "", "has_bzip_domain": False, "job_id": job_id}
        except (HTTPError, URLError, TimeoutError, KeyError, json.JSONDecodeError) as error:
            if attempt == 2:
                return {"protein_fasta_id": record.id, "status": f"error: {type(error).__name__}", "bzip_domain_hits": "", "has_bzip_domain": False, "job_id": ""}
            time.sleep(5 * (attempt + 1))
    raise AssertionError("unreachable")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=5)
    args = parser.parse_args()

    records = list(SeqIO.parse(args.input, "fasta"))
    results = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(scan_record, record): record.id for record in records}
        for index, future in enumerate(as_completed(futures), start=1):
            result = future.result()
            results.append(result)
            print(f"{index}/{len(records)} {result['protein_fasta_id']} {result['status']}", flush=True)

    table = pd.DataFrame(results).sort_values("protein_fasta_id")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(args.output, index=False)
    print(f"Confirmed bZIP domains: {table['has_bzip_domain'].sum()} / {len(table)}")


if __name__ == "__main__":
    main()

