"""Find Draper proteins homologous to the paper's confirmed VcbZIP reference proteins."""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

import pandas as pd
import pyhmmer


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--references", type=Path, required=True)
    parser.add_argument("--proteins", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cpus", type=int, default=8)
    parser.add_argument("--evalue", type=float, default=1e-5)
    args = parser.parse_args()

    alphabet = pyhmmer.easel.Alphabet.amino()
    with pyhmmer.easel.SequenceFile(args.references, digital=True, alphabet=alphabet) as handle:
        references = list(handle)
    with pyhmmer.easel.SequenceFile(args.proteins, digital=True, alphabet=alphabet) as handle:
        database = pyhmmer.easel.DigitalSequenceBlock(alphabet, list(handle))

    best_hits: dict[str, dict[str, object]] = {}
    source_queries: defaultdict[str, set[str]] = defaultdict(set)
    for index, (query, hits) in enumerate(
        zip(references, pyhmmer.hmmer.phmmer(references, database, cpus=args.cpus, E=args.evalue)), start=1
    ):
        for hit in hits:
            target = str(hit.name)
            source_queries[target].add(str(query.name))
            current = best_hits.get(target)
            if current is None or hit.evalue < current["best_evalue"]:
                best_hits[target] = {
                    "protein_fasta_id": target,
                    "best_evalue": hit.evalue,
                    "best_score": hit.score,
                    "best_query": str(query.name),
                }
        print(f"{index}/{len(references)} queries processed; {len(best_hits)} unique candidates")

    rows = []
    for target, values in best_hits.items():
        values["matching_reference_queries"] = ";".join(sorted(source_queries[target]))
        values["reference_query_count"] = len(source_queries[target])
        rows.append(values)

    result = pd.DataFrame(rows).sort_values(["best_evalue", "protein_fasta_id"])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.output, index=False)
    print(f"Saved {len(result)} union candidates to {args.output}")


if __name__ == "__main__":
    main()

