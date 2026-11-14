"""Verify salt-responsive VcbZIP genes against source DESeq2 result blocks."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


COMPARISONS = [(0, "S6_vs_S0"), (15, "S12_vs_S0"), (30, "S24_vs_S0"), (45, "S48_vs_S0")]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bzip-workbook", type=Path, required=True)
    parser.add_argument("--source-workbook", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    bzip = pd.read_excel(args.bzip_workbook, sheet_name="Table S3", header=1).dropna(subset=["Gene_id"])
    raw = pd.read_excel(args.source_workbook, sheet_name="Table S7", header=None)
    source = {}
    for start, label in COMPARISONS:
        block = raw.iloc[3:, start : start + 14].copy()
        block.columns = raw.iloc[2, start : start + 14].tolist()
        block = block.dropna(subset=["gene_id"])
        block["log2FoldChange"] = pd.to_numeric(block["log2FoldChange"], errors="coerce")
        block["pvalue"] = pd.to_numeric(block["pvalue"], errors="coerce")
        source[label] = block.set_index("gene_id")

    rows = []
    for _, row in bzip.iterrows():
        gene_id = row["Gene_id"]
        found = []
        for label, block in source.items():
            if gene_id not in block.index:
                continue
            values = block.loc[gene_id]
            if abs(values["log2FoldChange"]) >= 1 and values["pvalue"] < 0.05:
                found.append(label)
        rows.append(
            {
                "gene_id": gene_id,
                "gene_name": row["Gene name"],
                "significant_source_comparisons": ";".join(found),
                "reproduced_as_salt_responsive": bool(found),
            }
        )

    result = pd.DataFrame(rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.output, index=False)
    print(f"Reproduced salt-responsive genes: {result['reproduced_as_salt_responsive'].sum()} / {len(result)}")


if __name__ == "__main__":
    main()

