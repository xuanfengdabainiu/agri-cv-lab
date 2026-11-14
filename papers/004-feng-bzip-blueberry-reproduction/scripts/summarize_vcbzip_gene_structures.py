"""Summarize exon, intron, and genomic span for paper VcbZIP gene copies."""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def parse_attributes(field: str) -> dict[str, str]:
    return dict(item.split("=", 1) for item in field.split(";") if "=" in item)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workbook", type=Path, required=True)
    parser.add_argument("--gff", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    table = pd.read_excel(args.workbook, sheet_name="Table S1", header=1).dropna(subset=["Gene ID", "Gene name"])
    gene_to_name = {
        gene_id.strip(): str(row["Gene name"])
        for _, row in table.iterrows()
        for gene_id in str(row["Gene ID"]).split("/")
    }
    genes: dict[str, dict[str, object]] = {}
    exons: defaultdict[str, list[tuple[int, int]]] = defaultdict(list)

    with args.gff.open(encoding="utf-8") as handle:
        for line in handle:
            if line.startswith("#"):
                continue
            fields = line.rstrip("\n").split("\t")
            if len(fields) != 9:
                continue
            feature = fields[2]
            attributes = parse_attributes(fields[8])
            if feature == "gene":
                gene_id = attributes.get("ID", "")
                if gene_id in gene_to_name:
                    genes[gene_id] = {
                        "paper_vcbzip_name": gene_to_name[gene_id],
                        "gene_id": gene_id,
                        "scaffold": fields[0],
                        "strand": fields[6],
                        "gene_start": int(fields[3]),
                        "gene_end": int(fields[4]),
                    }
            elif feature == "exon":
                parent = attributes.get("Parent", "").removesuffix("-mRNA-1")
                if parent in gene_to_name:
                    exons[parent].append((int(fields[3]), int(fields[4])))

    rows = []
    for gene_id, item in genes.items():
        exon_spans = sorted(set(exons[gene_id]))
        rows.append(
            {
                **item,
                "gene_span_bp": int(item["gene_end"]) - int(item["gene_start"]) + 1,
                "exon_count": len(exon_spans),
                "exon_total_bp": sum(end - start + 1 for start, end in exon_spans),
                "intron_count": max(0, len(exon_spans) - 1),
            }
        )

    result = pd.DataFrame(rows).sort_values(["paper_vcbzip_name", "gene_id"])
    args.output_dir.mkdir(parents=True, exist_ok=True)
    figures = args.output_dir / "figures"
    figures.mkdir(exist_ok=True)
    result.to_csv(args.output_dir / "vcbzip-gene-structures.csv", index=False)

    counts = result["exon_count"].value_counts().sort_index()
    counts.rename_axis("exon_count").reset_index(name="gene_copy_count").to_csv(args.output_dir / "vcbzip-exon-count-summary.csv", index=False)
    plt.figure(figsize=(7, 4))
    plt.bar(counts.index.astype(str), counts.values, color="#356fa0")
    plt.xlabel("Exon count per VcbZIP gene copy")
    plt.ylabel("Number of gene copies")
    plt.tight_layout()
    plt.savefig(figures / "vcbzip-exon-counts.png", dpi=200)
    plt.close()

    print(f"Gene copies summarized: {len(result)}")
    print(f"VcbZIP names represented: {result['paper_vcbzip_name'].nunique()}")
    print(f"Exon count range: {result['exon_count'].min()}-{result['exon_count'].max()}")
    print(counts.to_string())


if __name__ == "__main__":
    main()

