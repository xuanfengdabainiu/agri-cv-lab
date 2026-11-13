"""Map Feng et al. supplementary-table VcbZIP genes to Draper protein FASTA records."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from Bio import SeqIO


def normalise_gene_id(record_id: str) -> str:
    return record_id.removesuffix("-mRNA-1")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workbook", type=Path, required=True)
    parser.add_argument("--proteins", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    table = pd.read_excel(args.workbook, sheet_name="Table S1", header=1).dropna(subset=["Gene ID", "Gene name"])
    fasta_ids = {normalise_gene_id(record.id): record.id for record in SeqIO.parse(args.proteins, "fasta")}

    rows: list[dict[str, str]] = []
    for _, row in table.iterrows():
        for gene_id in str(row["Gene ID"]).split("/"):
            gene_id = gene_id.strip()
            rows.append(
                {
                    "vcbzip_name": str(row["Gene name"]),
                    "paper_gene_id": gene_id,
                    "protein_fasta_id": fasta_ids.get(gene_id, ""),
                    "found_in_fasta": str(gene_id in fasta_ids),
                }
            )

    result = pd.DataFrame(rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.output, index=False)
    print(f"VcbZIP names: {result['vcbzip_name'].nunique()}")
    print(f"Paper gene IDs: {len(result)}")
    print(f"Matched FASTA records: {result['found_in_fasta'].eq('True').sum()}")
    print(f"Missing FASTA records: {result['found_in_fasta'].eq('False').sum()}")


if __name__ == "__main__":
    main()

