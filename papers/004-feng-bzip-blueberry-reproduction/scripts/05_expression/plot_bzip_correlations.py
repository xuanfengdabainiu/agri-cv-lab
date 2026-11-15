"""Plot recomputed salt or drought VcbZIP Pearson correlation matrices."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    matrix = pd.read_csv(args.input, index_col=0)
    plt.figure(figsize=(max(7, len(matrix) * 0.55), max(6, len(matrix) * 0.5)))
    sns.heatmap(matrix, cmap="vlag", center=0, vmin=-1, vmax=1, square=True, linewidths=0.2, cbar_kws={"label": "Pearson r"})
    plt.title(args.title)
    plt.tight_layout()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(args.output, dpi=200)
    plt.close()


if __name__ == "__main__":
    main()

