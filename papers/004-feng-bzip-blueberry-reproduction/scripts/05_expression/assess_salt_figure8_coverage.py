"""Assess whether public salt DEG blocks cover enough data for Table S8 correlations."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


COMPARISONS = [(0, "S6_vs_S0"), (15, "S12_vs_S0"), (30, "S24_vs_S0"), (45, "S48_vs_S0")]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bzip-workbook", type=Path, required=True)
    parser.add_argument("--source-workbook", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    target = pd.read_excel(args.bzip_workbook, sheet_name="Table S8", header=1).dropna(subset=["Gene_id"])
    raw = pd.read_excel(args.source_workbook, sheet_name="Table S7", header=None)
    source_sets = {}
    for start, label in COMPARISONS:
        source_sets[label] = set(raw.iloc[3:, start].dropna().astype(str))

    rows = []
    for _, row in target.iterrows():
        ids = str(row["Gene_id"]).split("/")
        coverage = {label: any(gene_id in genes for gene_id in ids) for label, genes in source_sets.items()}
        rows.append({"gene_id": row["Gene_id"], "gene_name": row["Gene name"], "gene_family": row["Gene family"], **coverage, "treatment_timepoints_available": sum(coverage.values())})
    result = pd.DataFrame(rows)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    figures = args.output_dir / "figures"
    figures.mkdir(exist_ok=True)
    result.to_csv(args.output_dir / "salt-figure8-source-coverage.csv", index=False)

    coverage_counts = result["treatment_timepoints_available"].value_counts().sort_index()
    coverage_counts.rename_axis("available_treatment_timepoints").reset_index(name="stress_gene_count").to_csv(args.output_dir / "salt-figure8-source-coverage-summary.csv", index=False)
    plt.figure(figsize=(6, 4))
    plt.bar(coverage_counts.index.astype(str), coverage_counts.values, color="#8f5b34")
    plt.xlabel("Available salt-treatment time points in public DEG blocks")
    plt.ylabel("Stress-responsive genes from Table S8")
    plt.tight_layout()
    plt.savefig(figures / "salt-figure8-source-coverage.png", dpi=200)
    plt.close()
    print(f"Stress genes in Table S8: {len(result)}")
    print(f"Genes with all four salt-treatment time points: {(result['treatment_timepoints_available'] == 4).sum()}")
    print(coverage_counts.to_string())


if __name__ == "__main__":
    main()

