"""Plot reported versus recomputed correlation coefficients."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    table = pd.read_csv(args.input).dropna(subset=["recomputed_r"])
    close = table["absolute_difference"] <= 0.001
    plt.figure(figsize=(6, 6))
    plt.scatter(table.loc[close, "reported_r"], table.loc[close, "recomputed_r"], s=20, alpha=0.75, color="#2f7f5f", label="difference <= 0.001")
    plt.scatter(table.loc[~close, "reported_r"], table.loc[~close, "recomputed_r"], s=25, alpha=0.85, color="#c95d3b", label="larger difference")
    plt.plot([-1, 1], [-1, 1], "--", color="black", linewidth=1)
    plt.xlim(-1.05, 1.05)
    plt.ylim(-1.05, 1.05)
    plt.xlabel("Reported Pearson r")
    plt.ylabel("Recomputed Pearson r")
    plt.title("Drought VcbZIP-stress gene correlation verification")
    plt.legend(frameon=False)
    plt.tight_layout()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(args.output, dpi=200)
    plt.close()


if __name__ == "__main__":
    main()

