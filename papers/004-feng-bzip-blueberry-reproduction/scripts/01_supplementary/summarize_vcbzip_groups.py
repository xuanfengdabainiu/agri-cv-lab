"""Recover Table S1 VcbZIP group assignments and summarize gene structures by group."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workbook", type=Path, required=True)
    parser.add_argument("--gene-structures", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    table = pd.read_excel(args.workbook, sheet_name="Table S1", header=1).dropna(subset=["Gene ID", "Gene name"])
    groups = table[["Gene name", "Groups"]].copy()
    groups["group"] = groups["Groups"].ffill()
    groups = groups.drop(columns="Groups").rename(columns={"Gene name": "vcbzip_name"})
    structures = pd.read_csv(args.gene_structures)
    copy_groups = structures.merge(groups, how="left", left_on="paper_vcbzip_name", right_on="vcbzip_name")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    figures = args.output_dir / "figures"
    figures.mkdir(exist_ok=True)
    groups.to_csv(args.output_dir / "vcbzip-author-groups.csv", index=False)
    group_summary = groups["group"].value_counts().rename_axis("group").reset_index(name="vcbzip_name_count")
    group_summary.to_csv(args.output_dir / "vcbzip-group-summary.csv", index=False)
    copy_groups.to_csv(args.output_dir / "vcbzip-copy-structures-with-groups.csv", index=False)

    structure_summary = copy_groups.groupby("group")["exon_count"].agg(["count", "min", "median", "mean", "max"]).reset_index()
    structure_summary.to_csv(args.output_dir / "vcbzip-group-exon-summary.csv", index=False)

    ordered_groups = group_summary.sort_values("vcbzip_name_count", ascending=False)["group"].tolist()
    plt.figure(figsize=(7, 4))
    sns.barplot(data=group_summary, x="group", y="vcbzip_name_count", order=ordered_groups, color="#3f7d9c")
    plt.xlabel("Author-assigned bZIP group")
    plt.ylabel("Number of VcbZIP names")
    plt.tight_layout()
    plt.savefig(figures / "vcbzip-group-counts.png", dpi=200)
    plt.close()

    plt.figure(figsize=(9, 4.5))
    sns.boxplot(data=copy_groups, x="group", y="exon_count", order=ordered_groups, color="#b8d5e3")
    sns.stripplot(data=copy_groups, x="group", y="exon_count", order=ordered_groups, color="#244b63", size=3, alpha=0.65)
    plt.xlabel("Author-assigned bZIP group")
    plt.ylabel("Exon count per gene copy")
    plt.tight_layout()
    plt.savefig(figures / "vcbzip-group-exon-counts.png", dpi=200)
    plt.close()

    print(group_summary.to_string(index=False))
    print(structure_summary.to_string(index=False))


if __name__ == "__main__":
    main()

