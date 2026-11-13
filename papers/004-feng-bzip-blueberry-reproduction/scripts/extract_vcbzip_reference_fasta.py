"""Extract the paper's confirmed VcbZIP protein sequences from the Draper proteome."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from Bio import SeqIO


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workbook", type=Path, required=True)
    parser.add_argument("--proteins", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    table = pd.read_excel(args.workbook, sheet_name="Table S1", header=1).dropna(subset=["Gene ID", "Gene name"])
    paper_ids = {
        gene_id.strip()
        for gene_ids in table["Gene ID"].astype(str)
        for gene_id in gene_ids.split("/")
    }
    records = [
        record
        for record in SeqIO.parse(args.proteins, "fasta")
        if record.id.removesuffix("-mRNA-1") in paper_ids
    ]

    args.output.parent.mkdir(parents=True, exist_ok=True)
    SeqIO.write(records, args.output, "fasta")
    print(f"Extracted {len(records)} reference proteins for {len(paper_ids)} paper gene IDs.")


if __name__ == "__main__":
    main()

