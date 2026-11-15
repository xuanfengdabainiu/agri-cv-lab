"""Draw bZIP expression heatmaps from verified source-study FPKM matrices."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


MODES = {
    "drought": {
        "source_sheet": "Table S2",
        "source_id": "Gene_id",
        "bzip_sheet": "Table S4",
        "bzip_id": "Gene_id",
        "timepoints": ["P0", "P6", "P12", "P24", "P48"],
        "source_column": lambda time, rep: f"{time}-{rep}_FPKM",
    },
    "aba": {
        "source_sheet": "Table S3",
        "source_id": "Gene ID",
        "bzip_sheet": "Table S5",
        "bzip_id": "Gene_id",
        "timepoints": ["0 h", "6 h", "12 h"],
        "source_column": lambda time, rep: f"{time} rep {rep} FPKM",
    },
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=MODES, required=True)
    parser.add_argument("--bzip-workbook", type=Path, required=True)
    parser.add_argument("--source-workbook", type=Path, required=True)
    parser.add_argument("--verification", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    config = MODES[args.mode]
    verification = pd.read_csv(args.verification)
    matched_ids = set(verification.loc[verification["source_status"] == "matched", "gene_id"])
    bzip = pd.read_excel(args.bzip_workbook, sheet_name=config["bzip_sheet"], header=1).dropna(subset=[config["bzip_id"]])
    names = bzip.set_index(config["bzip_id"])["Gene name"]
    source = pd.read_excel(args.source_workbook, sheet_name=config["source_sheet"], header=1).dropna(subset=[config["source_id"]]).set_index(config["source_id"])

    values = pd.DataFrame(index=sorted(matched_ids))
    for timepoint in config["timepoints"]:
        columns = [config["source_column"](timepoint, rep) for rep in range(1, 4)]
        values[timepoint] = source.loc[values.index, columns].apply(pd.to_numeric, errors="coerce").mean(axis=1)
    values.index = [names[gene_id] for gene_id in values.index]

    args.output_dir.mkdir(parents=True, exist_ok=True)
    figures = args.output_dir / "figures"
    figures.mkdir(exist_ok=True)
    values.to_csv(args.output_dir / f"{args.mode}-verified-source-mean-fpkm.csv")

    plt.figure(figsize=(8, max(4, len(values) * 0.4)))
    sns.heatmap(np.log10(values + 1), cmap="viridis", linewidths=0.25, cbar_kws={"label": "log10(mean FPKM + 1)"})
    plt.title(f"Verified source-study VcbZIP expression under {args.mode} stress")
    plt.xlabel("Treatment time point")
    plt.ylabel("VcbZIP gene")
    plt.tight_layout()
    plt.savefig(figures / f"{args.mode}-verified-source-heatmap.png", dpi=200)
    plt.close()
    print(f"Plotted {len(values)} verified {args.mode} VcbZIP genes.")


if __name__ == "__main__":
    main()

