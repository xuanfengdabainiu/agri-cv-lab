"""Compare paper-reference and additional bZIP-domain candidates."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from Bio import SeqIO


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--proteins", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    table = pd.read_csv(args.candidates)
    lengths = {record.id: len(record.seq) for record in SeqIO.parse(args.proteins, "fasta")}
    table["protein_length_aa"] = table["protein_fasta_id"].map(lengths)
    table["is_shorter_than_100aa"] = table["protein_length_aa"] < 100
    table["is_longer_than_1000aa"] = table["protein_length_aa"] > 1000
    table = table.sort_values(["classification", "protein_length_aa", "protein_fasta_id"])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(args.output, index=False)

    summary = (
        table.groupby("classification")["protein_length_aa"]
        .agg(["count", "min", "median", "mean", "max"])
        .reset_index()
    )
    summary["shorter_than_100aa"] = [
        int(table.loc[table["classification"] == label, "is_shorter_than_100aa"].sum())
        for label in summary["classification"]
    ]
    summary["longer_than_1000aa"] = [
        int(table.loc[table["classification"] == label, "is_longer_than_1000aa"].sum())
        for label in summary["classification"]
    ]
    summary.to_csv(args.summary, index=False)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()

