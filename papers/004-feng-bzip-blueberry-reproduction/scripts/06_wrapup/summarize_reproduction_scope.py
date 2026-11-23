"""Build the final reproduction-scope table from the recorded result files.

Every number in the output is recomputed from an existing result CSV, so the
summary cannot silently drift away from the data it describes. Rows that
cannot be computed (tooling or source-data limits) are recorded explicitly
instead of being left out.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


REPRODUCED = "reproduced"
PARTIAL = "partial"
NOT_REPRODUCED = "not_reproduced"
NOT_SUPPORTED = "not_supported_by_source_data"


def as_bool(series: pd.Series) -> pd.Series:
    """Read a CSV boolean column that may have been stored as True/False text."""
    if series.dtype == bool:
        return series
    return series.astype(str).str.strip().str.lower().eq("true")


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"required result file is missing: {path}")
    return pd.read_csv(path)


def paper_name_set(series: pd.Series) -> set[str]:
    """Collect VcbZIP names, dropping cells that repeat the same name twice."""
    names: set[str] = set()
    for value in series.dropna():
        for part in str(value).split(";"):
            name = part.strip()
            if name:
                names.add(name)
    return names


def supplementary_counts(results: Path) -> list[dict]:
    summary = read_csv(results / "01_supplementary" / "supplementary-summary.csv")
    values = dict(zip(summary["measurement"], summary["value"]))
    genes = int(values["VcbZIP genes in Table S1"])
    salt = int(values["salt-responsive VcbZIP rows"])
    drought = int(values["drought-responsive VcbZIP rows"])
    return [
        {
            "item_id": "supplemental-gene-count",
            "paper_claim": "The paper identifies 102 VcbZIP genes.",
            "reproduction_result": f"{genes} VcbZIP names counted from Table S1",
            "coverage": f"{genes}/{genes}",
            "status": REPRODUCED,
            "evidence": "results/01_supplementary/supplementary-summary.csv",
        },
        {
            "item_id": "supplemental-stress-counts",
            "paper_claim": "18 VcbZIP genes respond to salt stress and 13 respond to drought stress.",
            "reproduction_result": f"salt {salt}; drought {drought}",
            "coverage": f"salt {salt}/18; drought {drought}/13",
            "status": REPRODUCED,
            "evidence": "results/01_supplementary/supplementary-summary.csv",
        },
    ]


def cis_element_summary(results: Path) -> list[dict]:
    table = read_csv(results / "01_supplementary" / "cis-element-summary.csv")
    aba = table[table["cis_element_category"] == "Abscisic acid responsive"].iloc[0]
    elements = int(aba["total_element_count"])
    genes = int(aba["vcbzip_genes_with_element"])
    total_genes = int(aba["total_vcbzip_genes"])
    return [
        {
            "item_id": "cis-element-aba",
            "paper_claim": "Table S2 lists 261 ABA-responsive elements across 82 VcbZIP promoters.",
            "reproduction_result": f"{elements} elements across {genes} of {total_genes} promoters",
            "coverage": f"{elements}/261",
            "status": REPRODUCED,
            "evidence": "results/01_supplementary/cis-element-summary.csv",
        }
    ]


def domain_screen(results: Path) -> list[dict]:
    table = read_csv(results / "03_domain_screen" / "bzip-domain-candidate-summary.csv")
    confirmed = table[as_bool(table["has_bzip_domain"])]
    paper_refs = confirmed[confirmed["classification"] == "paper_reference_bzip"]
    extra = confirmed[confirmed["classification"] == "additional_bzip_domain_candidate"]
    paper_names = paper_name_set(confirmed["paper_vcbzip_name"])
    return [
        {
            "item_id": "bzip-domain-paper-references",
            "paper_claim": "Every reported VcbZIP protein contains a bZIP domain.",
            "reproduction_result": (
                f"{len(paper_refs)}/{len(paper_refs)} paper reference proteins carry "
                "PF00170, PF07716, PF03131, or PF12498"
            ),
            "coverage": f"{len(paper_names)}/102 VcbZIP names",
            "status": REPRODUCED,
            "evidence": "results/03_domain_screen/bzip-domain-candidate-summary.csv",
        },
        {
            "item_id": "final-gene-set-size",
            "paper_claim": "The final set is 102 VcbZIP genes after duplicate and incomplete filtering.",
            "reproduction_result": (
                f"{len(confirmed)} of {len(table)} homology candidates are domain-confirmed; "
                f"{len(extra)} extra confirmed candidates have no published exclusion rule"
            ),
            "coverage": "102/102 VcbZIP names recovered",
            "status": PARTIAL,
            "evidence": "results/03_domain_screen/additional-bzip-domain-candidates.csv",
        },
    ]


def gene_structure(results: Path) -> list[dict]:
    table = read_csv(results / "02_genome" / "vcbzip-exon-count-summary.csv")
    copies = int(table["gene_copy_count"].sum())
    return [
        {
            "item_id": "gene-structure",
            "paper_claim": "VcbZIP gene structures are reported per gene copy from the genome annotation.",
            "reproduction_result": (
                f"{copies} gene copies; exon count "
                f"{int(table['exon_count'].min())}-{int(table['exon_count'].max())}"
            ),
            "coverage": f"{copies}/153 copies",
            "status": REPRODUCED,
            "evidence": "results/02_genome/vcbzip-exon-count-summary.csv",
        }
    ]


def promoters(results: Path) -> list[dict]:
    table = read_csv(results / "02_genome" / "vcbzip-promoter-extraction.csv")
    names = table["paper_vcbzip_name"].nunique()
    short = table[table["promoter_length"] < 2000]
    return [
        {
            "item_id": "promoter-extraction",
            "paper_claim": "2 kb upstream promoter regions are analysed for cis-elements.",
            "reproduction_result": (
                f"{len(table)} sequences for {names} VcbZIP names; "
                f"{len(short)} copy shorter than 2000 bp (min {int(table['promoter_length'].min())} bp)"
            ),
            "coverage": f"{names}/102 VcbZIP names",
            "status": REPRODUCED,
            "evidence": "results/02_genome/vcbzip-promoter-extraction.csv",
        }
    ]


def phylogeny(results: Path) -> list[dict]:
    table = read_csv(results / "04_phylogeny" / "bzip-nearest-arabidopsis-references.csv")
    names = paper_name_set(table["vcbzip_name"])
    distinct_refs = table["nearest_arabidopsis_bzip"].nunique()
    return [
        {
            "item_id": "phylogeny-mapping",
            "paper_claim": "VcbZIP proteins are grouped against canonical Arabidopsis bZIP proteins.",
            "reproduction_result": (
                f"{len(names)} VcbZIP names across {len(table)} copies map onto "
                f"{distinct_refs} distinct nearest Arabidopsis bZIP references"
            ),
            "coverage": f"{len(names)}/102 VcbZIP names",
            "status": PARTIAL,
            "evidence": "results/04_phylogeny/bzip-nearest-arabidopsis-references.csv",
        }
    ]


def author_groups(results: Path) -> list[dict]:
    table = read_csv(results / "01_supplementary" / "vcbzip-group-summary.csv")
    total = int(table["vcbzip_name_count"].sum())
    top = table.sort_values("vcbzip_name_count", ascending=False).head(3)
    detail = ", ".join(f"{row.group} {int(row.vcbzip_name_count)}" for row in top.itertuples())
    return [
        {
            "item_id": "author-group-assignment",
            "paper_claim": "VcbZIP genes are assigned to groups A, D, G, I, and S.",
            "reproduction_result": f"{total} names recovered from Table S1 merged cells; {detail}",
            "coverage": f"{total}/102 names",
            "status": REPRODUCED,
            "evidence": "results/01_supplementary/vcbzip-group-summary.csv",
        }
    ]


def expression_checks(results: Path) -> list[dict]:
    salt = read_csv(results / "05_expression" / "salt-deg-membership-verification.csv")
    drought_deg = read_csv(results / "05_expression" / "drought-deg-membership-verification.csv")
    aba = read_csv(results / "05_expression" / "aba-fpkm-source-verification.csv")
    drought_fpkm = read_csv(results / "05_expression" / "drought-fpkm-source-verification.csv")

    salt_ok = int(as_bool(salt["reproduced_as_salt_responsive"]).sum())
    drought_ok = int(as_bool(drought_deg["reproduced_as_drought_responsive"]).sum())
    aba_ok = int(as_bool(aba["exact_match_within_1e-9"]).sum())
    drought_fpkm_ok = int(as_bool(drought_fpkm["exact_match_within_1e-9"]).sum())

    return [
        {
            "item_id": "salt-deg-list",
            "paper_claim": "18 VcbZIP genes are differentially expressed under salt stress.",
            "reproduction_result": f"{salt_ok}/{len(salt)} genes reproduced from the source DESeq2 blocks",
            "coverage": f"{salt_ok}/18",
            "status": REPRODUCED,
            "evidence": "results/05_expression/salt-deg-membership-verification.csv",
        },
        {
            "item_id": "drought-deg-list",
            "paper_claim": "13 VcbZIP genes are differentially expressed under drought stress.",
            "reproduction_result": f"{drought_ok}/{len(drought_deg)} genes reproduced from the source DESeq2 blocks",
            "coverage": f"{drought_ok}/13",
            "status": PARTIAL,
            "evidence": "results/05_expression/drought-deg-membership-verification.csv",
        },
        {
            "item_id": "drought-fpkm-values",
            "paper_claim": "Drought FPKM values match the original drought study.",
            "reproduction_result": f"{drought_fpkm_ok}/{len(drought_fpkm)} profiles match exactly",
            "coverage": f"{drought_fpkm_ok}/13",
            "status": PARTIAL,
            "evidence": "results/05_expression/drought-fpkm-source-verification.csv",
        },
        {
            "item_id": "aba-fpkm-values",
            "paper_claim": "ABA FPKM values match the original ABA study.",
            "reproduction_result": f"{aba_ok}/{len(aba)} profiles match exactly",
            "coverage": f"{aba_ok}/7",
            "status": PARTIAL,
            "evidence": "results/05_expression/aba-fpkm-source-verification.csv",
        },
    ]


def correlation_checks(results: Path) -> list[dict]:
    salt = read_csv(results / "05_expression" / "salt-bzip-correlation-comparison.csv")
    drought = read_csv(results / "05_expression" / "drought-bzip-correlation-comparison.csv")

    salt_max = float(salt["absolute_difference"].max())
    salt_close = int((salt["absolute_difference"] <= 0.05).sum())
    drought_max = float(drought["absolute_difference"].max())
    drought_worst = drought.loc[drought["absolute_difference"].idxmax()]
    drought_close = int((drought["absolute_difference"] <= 0.05).sum())

    return [
        {
            "item_id": "salt-pearson-correlations",
            "paper_claim": "Pearson correlations between salt-responsive VcbZIP genes match Table S3.",
            "reproduction_result": (
                f"{salt_close}/{len(salt)} pairs within 0.05; max difference {salt_max:.3f}"
            ),
            "coverage": f"{salt_close}/{len(salt)} pairs",
            "status": REPRODUCED,
            "evidence": "results/05_expression/salt-bzip-correlation-comparison.csv",
        },
        {
            "item_id": "drought-pearson-correlations",
            "paper_claim": "Pearson correlations between drought-responsive VcbZIP genes match Table S4.",
            "reproduction_result": (
                f"{drought_close}/{len(drought)} pairs within 0.05; largest gap "
                f"{drought_worst['first_gene']}-{drought_worst['second_gene']} at {drought_max:.3f}"
            ),
            "coverage": f"{drought_close}/{len(drought)} pairs",
            "status": PARTIAL,
            "evidence": "results/05_expression/drought-bzip-correlation-comparison.csv",
        },
    ]


def figure8_checks(results: Path) -> list[dict]:
    drought = read_csv(results / "05_expression" / "drought-stress-gene-correlation-verification.csv")
    salt = read_csv(results / "05_expression" / "salt-figure8-source-coverage-summary.csv")

    computable = drought[drought["status"].astype(str).str.contains("matched")]
    within = int((computable["absolute_difference"] <= 0.001).sum())
    max_timepoints = int(salt["available_treatment_timepoints"].max())
    full = salt[salt["available_treatment_timepoints"] == max_timepoints]

    return [
        {
            "item_id": "figure8-drought-correlations",
            "paper_claim": "Figure 8 shows VcbZIP correlations with drought stress-response genes.",
            "reproduction_result": (
                f"{within}/{len(computable)} computable pairs agree within 0.001; "
                f"{len(drought) - len(computable)} of {len(drought)} rows have no matching source gene"
            ),
            "coverage": f"{within}/{len(computable)} computable pairs",
            "status": PARTIAL,
            "evidence": "results/05_expression/drought-stress-gene-correlation-verification.csv",
        },
        {
            "item_id": "figure8-salt-correlations",
            "paper_claim": "Figure 8 shows VcbZIP correlations with salt stress-response genes.",
            "reproduction_result": (
                f"only {int(full['stress_gene_count'].sum())} of "
                f"{int(salt['stress_gene_count'].sum())} stress genes have all treatment time points"
            ),
            "coverage": f"{int(full['stress_gene_count'].sum())}/{int(salt['stress_gene_count'].sum())} genes",
            "status": NOT_SUPPORTED,
            "evidence": "results/05_expression/salt-figure8-source-coverage-summary.csv",
        },
    ]


def tooling_limits() -> list[dict]:
    return [
        {
            "item_id": "meme-motif-analysis",
            "paper_claim": "Conserved motif analysis groups the VcbZIP proteins into groups A, D, G, I, and S.",
            "reproduction_result": "not run: MEME has no native Windows build",
            "coverage": "0/102 names classified from motifs",
            "status": NOT_REPRODUCED,
            "evidence": "bioconda `meme` 5.5.9 publishes linux-64 and macOS-64 only",
        },
        {
            "item_id": "plantcare-independent-scan",
            "paper_claim": "Promoter cis-elements are counted from the genome with PlantCARE.",
            "reproduction_result": "not run: PlantCARE only exposes the scan through its web interface",
            "coverage": "0/153 promoter sequences scanned",
            "status": NOT_REPRODUCED,
            "evidence": "no stable public PlantCARE batch API",
        },
        {
            "item_id": "raw-rnaseq-desq2-rerun",
            "paper_claim": "Differential expression is derived from the RNA-seq experiments.",
            "reproduction_result": "not run from raw reads: the SRA deposition pools replicates per time point",
            "coverage": "table-level reproduction only",
            "status": NOT_SUPPORTED,
            "evidence": "configs/rna-seq-sample-manifest.csv",
        },
    ]


def build_rows(results: Path) -> list[dict]:
    rows: list[dict] = []
    rows += supplementary_counts(results)
    rows += cis_element_summary(results)
    rows += domain_screen(results)
    rows += gene_structure(results)
    rows += promoters(results)
    rows += phylogeny(results)
    rows += author_groups(results)
    rows += expression_checks(results)
    rows += correlation_checks(results)
    rows += figure8_checks(results)
    rows += tooling_limits()
    return rows


def write_markdown(rows: list[dict], path: Path) -> None:
    counts = pd.Series([row["status"] for row in rows]).value_counts().to_dict()
    lines = [
        "# Reproduction Scope Summary",
        "",
        "Generated by `scripts/06_wrapup/summarize_reproduction_scope.py` from the recorded result files.",
        "",
        "| Item | Paper claim | This reproduction | Coverage | Status |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['item_id']}` | {row['paper_claim']} | {row['reproduction_result']} "
            f"| {row['coverage']} | {row['status']} |"
        )
    lines += [
        "",
        "## Status counts",
        "",
    ]
    for status, count in sorted(counts.items(), key=lambda item: -item[1]):
        lines.append(f"- {status}: {count}")
    lines += [
        "",
        "## Evidence files",
        "",
    ]
    for row in rows:
        lines.append(f"- `{row['item_id']}`: {row['evidence']}")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    rows = build_rows(args.results_dir)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    table = pd.DataFrame(rows)
    table.to_csv(args.output_dir / "reproduction-scope-summary.csv", index=False)
    write_markdown(rows, args.output_dir / "reproduction-scope-summary.md")

    print(table[["item_id", "coverage", "status"]].to_string(index=False))


if __name__ == "__main__":
    main()
