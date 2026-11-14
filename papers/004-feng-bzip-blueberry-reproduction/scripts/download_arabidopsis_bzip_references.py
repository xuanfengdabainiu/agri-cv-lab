"""Download the 78 Arabidopsis bZIP reference proteins used by Feng et al. (2025)."""

from __future__ import annotations

import argparse
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.request import Request, urlopen

import pandas as pd
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord


# AtbZIP1-AtbZIP79, excluding the AtbZIP73 pseudogene.
ATBZIP_GENE_IDS = {
    1: "AT5G49450", 2: "AT2G18160", 3: "AT5G15830", 4: "AT1G59530", 5: "AT3G49760",
    6: "AT2G22850", 7: "AT4G37730", 8: "AT1G68880", 9: "AT5G24800", 10: "AT4G02640",
    11: "AT4G34590", 12: "AT2G41070", 13: "AT5G44080", 14: "AT4G35900", 15: "AT5G42910",
    16: "AT2G35530", 17: "AT2G40950", 18: "AT2G40620", 19: "AT4G35040", 20: "AT5G06950",
    21: "AT1G08320", 22: "AT1G22070", 23: "AT2G16770", 24: "AT3G51960", 25: "AT3G54620",
    26: "AT5G06960", 27: "AT2G17770", 28: "AT3G10800", 29: "AT4G38900", 30: "AT2G21230",
    31: "AT3G13150", 32: "AT2G12940", 33: "AT2G12900", 34: "AT2G42380", 35: "AT1G49720",
    36: "AT1G45249", 37: "AT4G34000", 38: "AT3G19290", 39: "AT2G36270", 40: "AT1G03970",
    41: "AT4G36730", 42: "AT3G30530", 43: "AT5G38800", 44: "AT1G75390", 45: "AT3G12250",
    46: "AT1G68640", 47: "AT5G65210", 48: "AT2G04038", 49: "AT3G56660", 50: "AT1G77920",
    51: "AT1G43700", 52: "AT1G06850", 53: "AT3G62420", 54: "AT4G01120", 55: "AT2G46270",
    56: "AT5G11260", 57: "AT5G10030", 58: "AT1G13600", 59: "AT2G31370", 60: "AT1G42990",
    61: "AT3G58120", 62: "AT1G19490", 63: "AT5G28770", 64: "AT3G17609", 65: "AT5G06839",
    66: "AT3G56850", 67: "AT3G44460", 68: "AT1G32150", 69: "AT1G06070", 70: "AT5G60830",
    71: "AT2G24340", 72: "AT5G07160", 74: "AT2G21235", 75: "AT5G08141", 76: "AT1G58110",
    77: "AT1G35490", 78: "AT4G06598", 79: "AT5G04840",
}


def get_json(url: str) -> dict:
    request = Request(url, headers={"Content-Type": "application/json", "User-Agent": "agri-cv-lab-bzip-reproduction/1.0"})
    with urlopen(request, timeout=60) as response:
        return json.load(response)


def get_text(url: str) -> str:
    request = Request(url, headers={"Content-Type": "text/x-fasta", "User-Agent": "agri-cv-lab-bzip-reproduction/1.0"})
    with urlopen(request, timeout=60) as response:
        return response.read().decode("utf-8")


def fetch(number: int, gene_id: str) -> tuple[dict[str, str], SeqRecord]:
    for attempt in range(3):
        try:
            lookup = get_json(f"https://rest.ensembl.org/lookup/id/{gene_id}?expand=1;content-type=application/json")
            transcript_id = lookup["canonical_transcript"].rstrip(".")
            fasta = get_text(f"https://rest.ensembl.org/sequence/id/{transcript_id}?type=protein;content-type=text/x-fasta")
            sequence = "".join(fasta.splitlines()[1:])
            record = SeqRecord(Seq(sequence), id=f"AtbZIP{number}", description=f"{gene_id}; canonical_transcript={transcript_id}")
            return {
                "atbzip_name": f"AtbZIP{number}",
                "arabidopsis_gene_id": gene_id,
                "canonical_transcript_id": transcript_id,
                "protein_length_aa": str(len(sequence)),
            }, record
        except Exception:
            if attempt == 2:
                raise
            time.sleep(3 * (attempt + 1))
    raise AssertionError("unreachable")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-fasta", type=Path, required=True)
    parser.add_argument("--output-table", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=5)
    args = parser.parse_args()

    rows, records = [], []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(fetch, number, gene_id): number for number, gene_id in ATBZIP_GENE_IDS.items()}
        for index, future in enumerate(as_completed(futures), start=1):
            row, record = future.result()
            rows.append(row)
            records.append(record)
            print(f"{index}/{len(futures)} {row['atbzip_name']}", flush=True)

    records.sort(key=lambda record: int(record.id.removeprefix("AtbZIP")))
    args.output_fasta.parent.mkdir(parents=True, exist_ok=True)
    SeqIO.write(records, args.output_fasta, "fasta")
    pd.DataFrame(rows).sort_values("atbzip_name", key=lambda column: column.str.removeprefix("AtbZIP").astype(int)).to_csv(args.output_table, index=False)
    print(f"Downloaded {len(records)} Arabidopsis bZIP reference proteins.")


if __name__ == "__main__":
    main()

