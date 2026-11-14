"""Build an initial UPGMA tree from blueberry and Arabidopsis bZIP proteins."""

from __future__ import annotations

import argparse
from pathlib import Path

from Bio import AlignIO, Phylo, SeqIO
from Bio.Align import MultipleSeqAlignment
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from pyfamsa import Aligner, Sequence


def read_fasta(path: Path, prefix: str) -> list[tuple[str, str]]:
    return [(f"{prefix}{record.id}", str(record.seq)) for record in SeqIO.parse(path, "fasta")]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--blueberry", type=Path, required=True)
    parser.add_argument("--arabidopsis", type=Path, required=True)
    parser.add_argument("--alignment", type=Path, required=True)
    parser.add_argument("--tree", type=Path, required=True)
    parser.add_argument("--threads", type=int, default=8)
    args = parser.parse_args()

    raw_sequences = read_fasta(args.blueberry, "Vc|") + read_fasta(args.arabidopsis, "At|")
    famsa_sequences = [Sequence(identifier.encode(), sequence.encode()) for identifier, sequence in raw_sequences]
    aligner = Aligner(threads=args.threads)
    aligned = aligner.align(famsa_sequences)

    records = []
    for sequence in aligned:
        records.append(SeqRecord(Seq(sequence.sequence.decode()), id=sequence.id.decode(), description=""))
    msa = MultipleSeqAlignment(records)

    args.alignment.parent.mkdir(parents=True, exist_ok=True)
    AlignIO.write(msa, args.alignment, "fasta")
    calculator = DistanceCalculator("identity")
    distance_matrix = calculator.get_distance(msa)
    tree = DistanceTreeConstructor().upgma(distance_matrix)
    Phylo.write(tree, args.tree, "newick")
    print(f"Aligned {len(msa)} proteins across {msa.get_alignment_length()} columns.")
    print(f"Wrote UPGMA tree: {args.tree}")


if __name__ == "__main__":
    main()

