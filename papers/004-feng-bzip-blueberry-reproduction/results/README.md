# Results Index

`metrics.md` and `experiment-summary.md` are the project-level overview files. `06_wrapup/reproduction-scope-summary.md` is the final claim-by-claim scope table. Other outputs are grouped by analysis stage.

## 01_supplementary

Results reproduced directly from the paper and source-study supplementary workbooks.

- `supplementary-summary.csv`: VcbZIP, salt-response, and drought-response counts
- `salt-vcbzip-mean-fpkm.csv`, `drought-vcbzip-mean-fpkm.csv`: time-point FPKM matrices
- `cis-element-summary.csv`: promoter cis-element counts per category
- `vcbzip-author-groups.csv`, `vcbzip-group-summary.csv`: author group labels and counts
- `vcbzip-group-exon-summary.csv`, `vcbzip-copy-structures-with-groups.csv`: exon structure per group
- `figures/salt-vcbzip-heatmap.png`, `figures/drought-vcbzip-heatmap.png`
- `figures/cis-element-counts.png`, `figures/vcbzip-group-counts.png`, `figures/vcbzip-group-exon-counts.png`

## 02_genome

Results derived from the Draper V1.0 genome and GFF annotation.

- `vcbzip-promoter-extraction.csv`: promoter coordinates and lengths
- `vcbzip-gene-structures.csv`: per-copy exon, intron, and gene span
- `vcbzip-exon-count-summary.csv`: exon-count distribution
- `figures/vcbzip-exon-counts.png`

## 03_domain_screen

Results from bZIP homology screening and Pfam domain confirmation.

- `vcbzip-protein-mapping.csv`: paper gene-to-protein mapping
- `phmmer-bzip-candidates.csv`, `vcbzip1-phmmer-trial.tsv`: homology candidates and trial run
- `ebi-pfam-bzip-domain-confirmation.csv`: raw Pfam domain hits
- `bzip-domain-candidate-summary.csv`: merged domain hits with paper-reference membership
- `additional-bzip-domain-candidates.csv`, `bzip-domain-candidates-with-length.csv`, `bzip-candidate-length-summary.csv`: extra-candidate analysis

## 04_phylogeny

Results from the VcbZIP and Arabidopsis bZIP comparison.

- `arabidopsis-bzip-reference-mapping.csv`: reference protein metadata
- `bzip-blueberry-arabidopsis-alignment.fasta`: 231-sequence alignment
- `bzip-upgma-tree.nwk`: UPGMA tree
- `bzip-nearest-arabidopsis-references.csv`: nearest Arabidopsis reference per VcbZIP copy

## 05_expression

Results that verify the bZIP paper's stress-response tables against the original studies.

- `drought-fpkm-source-verification.csv`, `aba-fpkm-source-verification.csv`: FPKM verification
- `salt-aba-source-membership-verification.csv`: membership verification
- `drought-deg-membership-verification.csv`, `salt-deg-membership-verification.csv`: DEG list reproduction
- `drought-bzip-correlation-comparison.csv`, `salt-bzip-correlation-comparison.csv`: Pearson correlation comparison
- `drought-bzip-recomputed-correlation.csv`, `salt-bzip-recomputed-correlation.csv`: recomputed matrices
- `drought-bzip-timepoint-mean-fpkm.csv`, `salt-bzip-timepoint-mean-fpkm.csv`: time-point means
- `drought-verified-source-mean-fpkm.csv`, `aba-verified-source-mean-fpkm.csv`: verified source means
- `drought-stress-gene-correlation-verification.csv`: Table S9 check
- `salt-figure8-source-coverage.csv`, `salt-figure8-source-coverage-summary.csv`: Table S8 coverage assessment
- `figures/drought-verified-source-heatmap.png`, `figures/aba-verified-source-heatmap.png`
- `figures/salt-bzip-recomputed-correlation.png`, `figures/drought-bzip-recomputed-correlation.png`
- `figures/drought-stress-gene-correlation-verification.png`, `figures/salt-figure8-source-coverage.png`

## 06_wrapup

Final project close-out.

- `reproduction-scope-summary.md`: claim-by-claim scope table with status and evidence links
- `reproduction-scope-summary.csv`: the same table in machine-readable form

