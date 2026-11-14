"""Extract protein sequences for the phmmer bZIP candidate list."""

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
    args = parser.parse_args()

    candidate_ids = set(pd.read_csv(args.candidates)["protein_fasta_id"])
    records = [record for record in SeqIO.parse(args.proteins, "fasta") if record.id in candidate_ids]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    SeqIO.write(records, args.output, "fasta")

    if len(records) != len(candidate_ids):
        raise RuntimeError(f"Expected {len(candidate_ids)} sequences, extracted {len(records)}.")
    print(f"Extracted {len(records)} candidate proteins.")


if __name__ == "__main__":
    main()

