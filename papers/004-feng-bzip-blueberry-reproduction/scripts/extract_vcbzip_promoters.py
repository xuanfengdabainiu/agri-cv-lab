"""Extract 2 kb upstream promoter sequences for paper VcbZIP gene copies.

The paper defines promoters as the 2 kb upstream region from the ATG start.
For plus-strand genes this is upstream of the first CDS coordinate. For
minus-strand genes it is downstream of the last CDS coordinate, reverse
complemented into the gene's transcriptional orientation.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

import pandas as pd
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord


def parse_attributes(field: str) -> dict[str, str]:
    return dict(item.split("=", 1) for item in field.split(";") if "=" in item)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workbook", type=Path, required=True)
    parser.add_argument("--gff", type=Path, required=True)
    parser.add_argument("--genome", type=Path, required=True)
    parser.add_argument("--output-fasta", type=Path, required=True)
    parser.add_argument("--output-table", type=Path, required=True)
    parser.add_argument("--length", type=int, default=2000)
    args = parser.parse_args()

    table = pd.read_excel(args.workbook, sheet_name="Table S1", header=1).dropna(subset=["Gene ID", "Gene name"])
    gene_to_name: dict[str, str] = {}
    for _, row in table.iterrows():
        for gene_id in str(row["Gene ID"]).split("/"):
            gene_to_name[gene_id.strip()] = str(row["Gene name"])

    cds: dict[str, list[tuple[int, int]]] = defaultdict(list)
    metadata: dict[str, tuple[str, str]] = {}
    with args.gff.open(encoding="utf-8") as handle:
        for line in handle:
            if line.startswith("#"):
                continue
            fields = line.rstrip("\n").split("\t")
            if len(fields) != 9 or fields[2] != "CDS":
                continue
            attributes = parse_attributes(fields[8])
            parent = attributes.get("Parent", "")
            gene_id = parent.removesuffix("-mRNA-1")
            if gene_id not in gene_to_name:
                continue
            cds[gene_id].append((int(fields[3]), int(fields[4])))
            metadata[gene_id] = (fields[0], fields[6])

    by_scaffold: dict[str, list[str]] = defaultdict(list)
    for gene_id, (scaffold, _strand) in metadata.items():
        by_scaffold[scaffold].append(gene_id)

    rows: list[dict[str, object]] = []
    records = []
    for genome_record in SeqIO.parse(args.genome, "fasta"):
        for gene_id in by_scaffold.get(genome_record.id, []):
            scaffold, strand = metadata[gene_id]
            spans = cds[gene_id]
            if strand == "+":
                atg = min(start for start, _end in spans)
                start = max(1, atg - args.length)
                end = atg - 1
                sequence = genome_record.seq[start - 1 : end]
            else:
                atg = max(end for _start, end in spans)
                start = atg + 1
                end = min(len(genome_record.seq), atg + args.length)
                sequence = genome_record.seq[start - 1 : end].reverse_complement()

            record = SeqRecord(
                sequence,
                id=gene_id,
                description=f"{gene_to_name[gene_id]} scaffold={scaffold} strand={strand} ATG={atg} promoter_length={len(sequence)}",
            )
            records.append(record)
            rows.append(
                {
                    "paper_vcbzip_name": gene_to_name[gene_id],
                    "gene_id": gene_id,
                    "scaffold": scaffold,
                    "strand": strand,
                    "atg_coordinate": atg,
                    "promoter_start": start,
                    "promoter_end": end,
                    "promoter_length": len(sequence),
                }
            )

    missing = set(gene_to_name) - {row["gene_id"] for row in rows}
    if missing:
        raise RuntimeError(f"Could not extract promoters for {len(missing)} genes: {sorted(missing)[:5]}")

    args.output_fasta.parent.mkdir(parents=True, exist_ok=True)
    SeqIO.write(records, args.output_fasta, "fasta")
    pd.DataFrame(rows).sort_values(["paper_vcbzip_name", "gene_id"]).to_csv(args.output_table, index=False)
    print(f"Extracted {len(records)} promoter sequences for {len(set(gene_to_name.values()))} VcbZIP names.")
    print(f"Promoters shorter than {args.length} bp: {sum(row['promoter_length'] < args.length for row in rows)}")


if __name__ == "__main__":
    main()

