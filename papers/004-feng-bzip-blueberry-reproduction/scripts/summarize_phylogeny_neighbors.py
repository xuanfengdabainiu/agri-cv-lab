"""Find the nearest Arabidopsis bZIP reference for each blueberry tip in a tree."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from Bio import Phylo


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tree", type=Path, required=True)
    parser.add_argument("--mapping", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    tree = Phylo.read(args.tree, "newick")
    mapping = pd.read_csv(args.mapping).groupby("protein_fasta_id")["vcbzip_name"].agg(";".join)
    terminals = {terminal.name: terminal for terminal in tree.get_terminals()}
    arabidopsis = [name for name in terminals if name.startswith("At|AtbZIP")]
    rows = []
    for protein_id, vcbzip_name in mapping.items():
        tip_name = f"Vc|{protein_id}"
        if tip_name not in terminals:
            continue
        nearest = min(arabidopsis, key=lambda name: tree.distance(terminals[tip_name], terminals[name]))
        rows.append(
            {
                "vcbzip_name": vcbzip_name,
                "blueberry_protein_fasta_id": protein_id,
                "nearest_arabidopsis_bzip": nearest.removeprefix("At|"),
                "tree_distance": tree.distance(terminals[tip_name], terminals[nearest]),
            }
        )
    result = pd.DataFrame(rows).sort_values(["vcbzip_name", "blueberry_protein_fasta_id"])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.output, index=False)
    print(f"Mapped {len(result)} blueberry protein copies to nearest Arabidopsis references.")
    print(result["nearest_arabidopsis_bzip"].value_counts().head(15).to_string())


if __name__ == "__main__":
    main()

