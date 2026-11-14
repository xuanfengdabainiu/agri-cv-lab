"""Summarize Table S2 promoter cis-elements reported for VcbZIP genes."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workbook", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    table = pd.read_excel(args.workbook, sheet_name="Table S2", header=1).dropna(subset=["Gene name"])
    element_columns = [column for column in table.columns if column != "Gene name"]
    values = table[element_columns].apply(pd.to_numeric, errors="coerce").fillna(0)
    summary = pd.DataFrame(
        {
            "cis_element_category": element_columns,
            "total_element_count": values.sum().to_numpy(dtype=int),
            "vcbzip_genes_with_element": (values > 0).sum().to_numpy(dtype=int),
            "total_vcbzip_genes": len(table),
        }
    ).sort_values("total_element_count", ascending=False)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    figures = args.output_dir / "figures"
    figures.mkdir(exist_ok=True)
    summary.to_csv(args.output_dir / "cis-element-summary.csv", index=False)

    plot = summary.sort_values("total_element_count")
    plt.figure(figsize=(9, 5))
    plt.barh(plot["cis_element_category"], plot["total_element_count"], color="#3a7d44")
    plt.xlabel("Total predicted cis-elements across 102 VcbZIP promoters")
    plt.ylabel("Cis-element category")
    plt.tight_layout()
    plt.savefig(figures / "cis-element-counts.png", dpi=200)
    plt.close()
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()

