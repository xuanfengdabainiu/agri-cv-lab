"""Recompute bZIP Pearson correlations from Tables S3/S4 and compare S6/S7."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


CONFIG = {
    "salt": {"expression_sheet": "Table S3", "correlation_sheet": "Table S6", "prefix": "S"},
    "drought": {"expression_sheet": "Table S4", "correlation_sheet": "Table S7", "prefix": "P"},
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workbook", type=Path, required=True)
    parser.add_argument("--mode", choices=CONFIG, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    config = CONFIG[args.mode]

    expression = pd.read_excel(args.workbook, sheet_name=config["expression_sheet"], header=1).dropna(subset=["Gene name"])
    timepoint_means = {}
    for time in ["0", "6", "12", "24", "48"]:
        label = f"{config['prefix']}{time}"
        columns = [column for column in expression.columns if str(column).startswith(f"{label}-") and "FPKM" in str(column)]
        timepoint_means[label] = expression[columns].astype(float).mean(axis=1).to_numpy()
    profiles = pd.DataFrame(timepoint_means, index=expression["Gene name"])
    recomputed = profiles.T.corr()

    reported = pd.read_excel(args.workbook, sheet_name=config["correlation_sheet"], header=1).dropna(subset=["Unnamed: 0"]).set_index("Unnamed: 0")
    rows = []
    names = list(profiles.index)
    for index, first in enumerate(names):
        for second in names[index + 1 :]:
            reported_value = float(str(reported.loc[first, second]).replace("*", ""))
            recomputed_value = recomputed.loc[first, second]
            rows.append(
                {
                    "first_gene": first,
                    "second_gene": second,
                    "reported_pearson_r": reported_value,
                    "recomputed_pearson_r": recomputed_value,
                    "absolute_difference": abs(recomputed_value - reported_value),
                }
            )

    differences = pd.DataFrame(rows).sort_values("absolute_difference", ascending=False)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    profiles.to_csv(args.output_dir / f"{args.mode}-bzip-timepoint-mean-fpkm.csv")
    recomputed.to_csv(args.output_dir / f"{args.mode}-bzip-recomputed-correlation.csv")
    differences.to_csv(args.output_dir / f"{args.mode}-bzip-correlation-comparison.csv", index=False)
    print(f"Pairs compared: {len(differences)}")
    print(f"Maximum absolute difference: {differences['absolute_difference'].max()}")
    print(differences.head(5).to_string(index=False))


if __name__ == "__main__":
    main()

