"""Verify Table S9 VcbZIP-stress gene correlations against source drought FPKM."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


TIMEPOINTS = ["P0", "P6", "P12", "P24", "P48"]


def parse_reported(value: object) -> float | None:
    text = str(value).strip()
    if text in {"--", "nan", ""}:
        return None
    return float(text.replace("*", ""))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bzip-workbook", type=Path, required=True)
    parser.add_argument("--source-workbook", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    bzip = pd.read_excel(args.bzip_workbook, sheet_name="Table S4", header=1).dropna(subset=["Gene_id"])
    correlations = pd.read_excel(args.bzip_workbook, sheet_name="Table S9", header=1).dropna(subset=["Gene_id"])
    source = pd.read_excel(args.source_workbook, sheet_name="Table S2", header=1).dropna(subset=["Gene_id"]).set_index("Gene_id")

    source_columns = [f"{time}-{rep}_FPKM" for time in TIMEPOINTS for rep in range(1, 4)]
    profiles = {}
    for _, row in bzip.iterrows():
        if row["Gene_id"] not in source.index:
            continue
        profiles[row["Gene name"]] = [source.loc[row["Gene_id"], [f"{time}-{rep}_FPKM" for rep in range(1, 4)]].astype(float).mean() for time in TIMEPOINTS]

    rows = []
    bzip_columns = [column for column in correlations.columns if column.startswith("VcbZIP")]
    for _, row in correlations.iterrows():
        target_ids = str(row["Gene_id"]).split("/")
        for bzip_name in bzip_columns:
            reported = parse_reported(row[bzip_name])
            if reported is None:
                continue
            if bzip_name not in profiles:
                rows.append({"stress_gene_name": row["Gene name"], "reported_bzip": bzip_name, "reported_r": reported, "source_gene_id": "", "recomputed_r": None, "absolute_difference": None, "status": "bzip_source_profile_missing"})
                continue

            candidates = []
            for target_id in target_ids:
                if target_id not in source.index:
                    continue
                target_profile = [source.loc[target_id, [f"{time}-{rep}_FPKM" for rep in range(1, 4)]].astype(float).mean() for time in TIMEPOINTS]
                calculated = float(np.corrcoef(profiles[bzip_name], target_profile)[0, 1])
                candidates.append((abs(calculated - reported), target_id, calculated))
            if not candidates:
                rows.append({"stress_gene_name": row["Gene name"], "reported_bzip": bzip_name, "reported_r": reported, "source_gene_id": "", "recomputed_r": None, "absolute_difference": None, "status": "stress_gene_source_profile_missing"})
                continue

            difference, target_id, calculated = min(candidates)
            rows.append({"stress_gene_name": row["Gene name"], "reported_bzip": bzip_name, "reported_r": reported, "source_gene_id": target_id, "recomputed_r": calculated, "absolute_difference": difference, "status": "matched"})

    result = pd.DataFrame(rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.output, index=False)
    matched = result.loc[result["status"] == "matched"]
    print(f"Reported correlations: {len(result)}")
    print(f"Source-computable correlations: {len(matched)}")
    print(f"Pairs within 0.001: {(matched['absolute_difference'] <= 0.001).sum()}")
    print(f"Maximum difference: {matched['absolute_difference'].max() if len(matched) else 'n/a'}")


if __name__ == "__main__":
    main()

