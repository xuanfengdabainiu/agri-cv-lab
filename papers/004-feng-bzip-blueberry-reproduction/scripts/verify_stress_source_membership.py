"""Verify bZIP stress-response lists against source-study supplementary tables."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def salt_verification(bzip_workbook: Path, salt_workbook: Path) -> pd.DataFrame:
    bzip = pd.read_excel(bzip_workbook, sheet_name="Table S3", header=1).dropna(subset=["Gene_id"])
    source = pd.read_excel(salt_workbook, sheet_name="Table S7", header=None)
    comparisons = {}
    for start, label in [(0, "S6_vs_S0"), (15, "S12_vs_S0"), (30, "S24_vs_S0"), (45, "S48_vs_S0")]:
        comparisons[label] = set(source.iloc[2:, start].dropna().astype(str))

    rows = []
    for _, row in bzip.iterrows():
        gene_id = str(row["Gene_id"])
        observed = [label for label, genes in comparisons.items() if gene_id in genes]
        rows.append({"stress": "salt", "gene_id": gene_id, "gene_name": row["Gene name"], "source_comparisons": ";".join(observed), "found_in_source": bool(observed)})
    return pd.DataFrame(rows)


def aba_verification(bzip_workbook: Path, aba_workbook: Path) -> pd.DataFrame:
    bzip = pd.read_excel(bzip_workbook, sheet_name="Table S5", header=1).dropna(subset=["Gene_id"])
    source = pd.read_excel(aba_workbook, sheet_name="Table S3", header=1).dropna(subset=["Gene ID"])
    source_ids = set(source["Gene ID"].astype(str))
    rows = []
    for _, row in bzip.iterrows():
        gene_id = str(row["Gene_id"])
        rows.append({"stress": "ABA", "gene_id": gene_id, "gene_name": row["Gene name"], "source_comparisons": "ABA hormone-pathway table", "found_in_source": gene_id in source_ids})
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bzip-workbook", type=Path, required=True)
    parser.add_argument("--salt-workbook", type=Path, required=True)
    parser.add_argument("--aba-workbook", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    result = pd.concat([salt_verification(args.bzip_workbook, args.salt_workbook), aba_verification(args.bzip_workbook, args.aba_workbook)], ignore_index=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.output, index=False)
    print(result.groupby("stress")["found_in_source"].agg(["sum", "count"]).to_string())


if __name__ == "__main__":
    main()

