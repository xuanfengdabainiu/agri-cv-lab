"""Assess extra domain-confirmed candidates against paper-reference bZIP proteins."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import pandas as pd
from Bio import SeqIO


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain-summary", type=Path, required=True)
    parser.add_argument("--homology", type=Path, required=True)
    parser.add_argument("--proteins", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    domains = pd.read_csv(args.domain_summary)
    homology = pd.read_csv(args.homology)[["protein_fasta_id", "best_evalue", "best_score", "best_query", "reference_query_count"]]
    sequences = {record.id: str(record.seq) for record in SeqIO.parse(args.proteins, "fasta")}
    domains = domains.merge(homology, on="protein_fasta_id", how="left")

    reference_hashes = {
        hashlib.sha256(sequences[row.protein_fasta_id].encode()).hexdigest()
        for row in domains.itertuples()
        if row.classification == "paper_reference_bzip"
    }
    extra = domains.loc[domains["classification"] == "additional_bzip_domain_candidate"].copy()
    extra["sequence_sha256"] = extra["protein_fasta_id"].map(lambda name: hashlib.sha256(sequences[name].encode()).hexdigest())
    extra["exact_duplicate_of_paper_reference"] = extra["sequence_sha256"].isin(reference_hashes)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    extra.sort_values(["exact_duplicate_of_paper_reference", "best_evalue", "protein_fasta_id"]).to_csv(args.output, index=False)

    print(f"Extra domain-confirmed candidates: {len(extra)}")
    print(f"Exact sequence duplicates of paper references: {extra['exact_duplicate_of_paper_reference'].sum()}")
    print(f"Candidates shorter than 100 aa: {(extra['protein_length_aa'] < 100).sum()}")


if __name__ == "__main__":
    main()

