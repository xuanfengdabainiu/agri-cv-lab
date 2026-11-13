"""Run a local phmmer trial from one confirmed VcbZIP protein against the Draper proteome."""

from __future__ import annotations

import argparse
from pathlib import Path

import pyhmmer


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=Path, required=True)
    parser.add_argument("--proteins", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cpus", type=int, default=4)
    parser.add_argument("--evalue", type=float, default=1e-5)
    args = parser.parse_args()

    alphabet = pyhmmer.easel.Alphabet.amino()
    with pyhmmer.easel.SequenceFile(args.query, digital=True, alphabet=alphabet) as handle:
        query = next(iter(handle))
    with pyhmmer.easel.SequenceFile(args.proteins, digital=True, alphabet=alphabet) as handle:
        database = pyhmmer.easel.DigitalSequenceBlock(alphabet, list(handle))

    hits = next(pyhmmer.hmmer.phmmer(query, database, cpus=args.cpus, E=args.evalue))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        handle.write("target_name\tevalue\tscore\tbias\n")
        for hit in hits:
            handle.write(f"{hit.name}\t{hit.evalue}\t{hit.score}\t{hit.bias}\n")
    print(f"Query: {query.name}")
    print(f"Hits at E <= {args.evalue}: {len(hits)}")


if __name__ == "__main__":
    main()

