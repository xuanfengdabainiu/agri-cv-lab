"""Summarize Feng et al. (2025) supplementary tables S1, S3, and S4."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def load_table(workbook: Path, sheet: str) -> pd.DataFrame:
    return pd.read_excel(workbook, sheet_name=sheet, header=1).dropna(how="all")


def expression_means(table: pd.DataFrame, prefix: str) -> pd.DataFrame:
    table = table.dropna(subset=["Gene name"]).copy()
    columns_by_time: dict[str, list[str]] = {}
    pattern = re.compile(rf"^({prefix}\d+)-\d+_FPKM(?:\.\d+)?$")

    for column in table.columns:
        match = pattern.match(str(column))
        if match:
            columns_by_time.setdefault(match.group(1), []).append(column)

    if not columns_by_time:
        raise ValueError(f"No {prefix} time-point FPKM columns found.")

    values = pd.DataFrame(index=table["Gene name"].astype(str).to_list())
    for time_point, columns in columns_by_time.items():
        values[time_point] = table[columns].apply(pd.to_numeric, errors="coerce").mean(axis=1).to_numpy()

    return values


def write_heatmap(values: pd.DataFrame, title: str, output: Path) -> None:
    plt.figure(figsize=(8, max(5, len(values) * 0.35)))
    sns.heatmap(
        np.log10(values + 1),
        cmap="viridis",
        linewidths=0.25,
        cbar_kws={"label": "log10(mean FPKM + 1)"},
    )
    plt.title(title)
    plt.xlabel("Treatment time point")
    plt.ylabel("VcbZIP gene")
    plt.tight_layout()
    plt.savefig(output, dpi=200)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workbook", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    figures_dir = args.output_dir / "figures"
    figures_dir.mkdir(exist_ok=True)

    basic = load_table(args.workbook, "Table S1")
    salt = load_table(args.workbook, "Table S3")
    drought = load_table(args.workbook, "Table S4")

    salt_means = expression_means(salt, "S")
    drought_means = expression_means(drought, "P")

    salt_means.to_csv(args.output_dir / "salt-vcbzip-mean-fpkm.csv")
    drought_means.to_csv(args.output_dir / "drought-vcbzip-mean-fpkm.csv")
    write_heatmap(salt_means, "Salt-stress VcbZIP expression", figures_dir / "salt-vcbzip-heatmap.png")
    write_heatmap(drought_means, "Drought-stress VcbZIP expression", figures_dir / "drought-vcbzip-heatmap.png")

    summary = pd.DataFrame(
        {
            "measurement": ["VcbZIP genes in Table S1", "salt-responsive VcbZIP rows", "drought-responsive VcbZIP rows"],
            "value": [basic["Gene name"].dropna().nunique(), salt_means.shape[0], drought_means.shape[0]],
        }
    )
    summary.to_csv(args.output_dir / "supplementary-summary.csv", index=False)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()

