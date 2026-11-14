"""Create a concise experiment manifest from downloaded SRA runinfo CSV files."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


PROJECT_LABELS = {
    "PRJNA1160404": "drought",
    "PRJNA1128395": "salt",
    "PRJNA997066": "ABA",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runinfo-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    manifests = []
    for project, label in PROJECT_LABELS.items():
        runinfo = pd.read_csv(args.runinfo_dir / f"{project}-runinfo.csv")
        manifests.append(
            pd.DataFrame(
                {
                    "analysis": label,
                    "bioproject": project,
                    "sample": runinfo["SampleName"],
                    "run": runinfo["Run"],
                    "library_name": runinfo["LibraryName"],
                    "size_mb": runinfo["size_MB"],
                    "bases": runinfo["bases"],
                    "platform": runinfo["Platform"],
                    "model": runinfo["Model"],
                    "layout": runinfo["LibraryLayout"],
                }
            )
        )
    manifest = pd.concat(manifests, ignore_index=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    manifest.to_csv(args.output, index=False)
    print(manifest.groupby("analysis").agg(runs=("run", "count"), total_size_mb=("size_mb", "sum")).to_string())


if __name__ == "__main__":
    main()

