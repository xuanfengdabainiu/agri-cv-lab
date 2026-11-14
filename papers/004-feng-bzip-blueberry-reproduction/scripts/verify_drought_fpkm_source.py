"""Verify bZIP drought FPKM values against the source drought-study workbook."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


TIMEPOINTS = ["P0", "P6", "P12", "P24", "P48"]
EXPECTED_COLUMNS = [f"{timepoint}-{rep}_FPKM" for timepoint in TIMEPOINTS for rep in range(1, 4)]


def bzip_value_columns(table: pd.DataFrame) -> list[str]:
    columns = []
    for timepoint in TIMEPOINTS:
        columns.extend([column for column in table.columns if str(column).startswith(f"{timepoint}-") and "FPKM" in str(column)])
    return columns


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bzip-workbook", type=Path, required=True)
    parser.add_argument("--source-workbook", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    bzip = pd.read_excel(args.bzip_workbook, sheet_name="Table S4", header=1).dropna(subset=["Gene_id"])
    source = pd.read_excel(args.source_workbook, sheet_name="Table S2", header=1).dropna(subset=["Gene_id"])
    source = source.set_index("Gene_id")
    bzip_columns = bzip_value_columns(bzip)

    rows = []
    for _, row in bzip.iterrows():
        gene_id = row["Gene_id"]
        if gene_id not in source.index:
            rows.append(
                {
                    "gene_id": gene_id,
                    "gene_name": row["Gene name"],
                    "source_status": "missing_from_source_matrix",
                    "max_absolute_difference": None,
                    "mean_absolute_difference": None,
                    "exact_match_within_1e-9": False,
                }
            )
            continue
        bzip_values = row[bzip_columns].astype(float).to_numpy()
        source_values = source.loc[gene_id, EXPECTED_COLUMNS].astype(float).to_numpy()
        delta = np.abs(bzip_values - source_values)
        rows.append(
            {
                "gene_id": gene_id,
                "gene_name": row["Gene name"],
                "source_status": "matched",
                "max_absolute_difference": delta.max(),
                "mean_absolute_difference": delta.mean(),
                "exact_match_within_1e-9": bool(np.all(delta < 1e-9)),
            }
        )

    result = pd.DataFrame(rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.output, index=False)
    print(f"Genes compared: {len(result)}")
    print(f"Exact FPKM matches: {result['exact_match_within_1e-9'].sum()}")
    print(f"Missing source rows: {(result['source_status'] != 'matched').sum()}")
    print(f"Maximum absolute difference: {result['max_absolute_difference'].max()}")


if __name__ == "__main__":
    main()

