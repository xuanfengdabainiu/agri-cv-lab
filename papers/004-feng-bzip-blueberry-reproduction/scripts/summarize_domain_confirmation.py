"""Merge domain-confirmation results with the paper's VcbZIP reference mapping."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--domains", type=Path, required=True)
    parser.add_argument("--mapping", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    domains = pd.read_csv(args.domains)
    mapping = pd.read_csv(args.mapping)
    paper_names = mapping.groupby("protein_fasta_id")["vcbzip_name"].agg(";".join).rename("paper_vcbzip_name")
    merged = domains.merge(paper_names, how="left", left_on="protein_fasta_id", right_index=True)
    merged["in_paper_reference_set"] = merged["paper_vcbzip_name"].notna()
    merged["classification"] = "similar_sequence_without_bzip_domain"
    merged.loc[merged["has_bzip_domain"] & ~merged["in_paper_reference_set"], "classification"] = "additional_bzip_domain_candidate"
    merged.loc[merged["has_bzip_domain"] & merged["in_paper_reference_set"], "classification"] = "paper_reference_bzip"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    merged.sort_values(["classification", "protein_fasta_id"]).to_csv(args.output, index=False)

    print(merged["classification"].value_counts().to_string())


if __name__ == "__main__":
    main()

