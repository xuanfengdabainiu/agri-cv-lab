"""Verify bZIP ABA FPKM values against the source ABA-study workbook."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


SOURCE_COLUMNS = [
    "0 h rep 1 FPKM", "0 h rep 2 FPKM", "0 h rep 3 FPKM",
    "6 h rep 1 FPKM", "6 h rep 2 FPKM", "6 h rep 3 FPKM",
    "12 h rep 1 FPKM", "12 h rep 2 FPKM", "12 h rep 3 FPKM",
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bzip-workbook", type=Path, required=True)
    parser.add_argument("--source-workbook", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    bzip = pd.read_excel(args.bzip_workbook, sheet_name="Table S5", header=1).dropna(subset=["Gene_id"])
    source = pd.read_excel(args.source_workbook, sheet_name="Table S3", header=1).dropna(subset=["Gene ID"]).set_index("Gene ID")
    bzip_columns = [column for column in bzip.columns if "FPKM" in str(column)]

    rows = []
    for _, row in bzip.iterrows():
        gene_id = row["Gene_id"]
        if gene_id not in source.index:
            rows.append({"gene_id": gene_id, "gene_name": row["Gene name"], "source_status": "missing_from_source_table", "max_absolute_difference": None, "exact_match_within_1e-9": False})
            continue
        delta = np.abs(row[bzip_columns].astype(float).to_numpy() - source.loc[gene_id, SOURCE_COLUMNS].astype(float).to_numpy())
        rows.append({"gene_id": gene_id, "gene_name": row["Gene name"], "source_status": "matched", "max_absolute_difference": delta.max(), "exact_match_within_1e-9": bool(np.all(delta < 1e-9))})

    result = pd.DataFrame(rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.output, index=False)
    print(f"Genes compared: {len(result)}")
    print(f"Exact FPKM matches: {result['exact_match_within_1e-9'].sum()}")
    print(f"Missing source rows: {(result['source_status'] != 'matched').sum()}")


if __name__ == "__main__":
    main()

