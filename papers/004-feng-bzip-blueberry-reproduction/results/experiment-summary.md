# Experiment Summary

## Current Status

The project has completed paper and data source inspection. The supplementary archive is available locally.

The first supplementary-table reproduction is complete. The following three sheets come from the paper's `supplementary tables.xlsx` file:

| Sheet | Original table title | What it contains | What we reproduced |
|---|---|---|---|
| Table S1 | Basic information about VcbZIP proteins in blueberry | The authors' identified VcbZIP genes, groups, protein sequences, lengths, and annotations | Counted 102 VcbZIP gene names |
| Table S3 | The differentially expressed VcbZIP genes under salt stress from transcriptome sequencing (RNA-Seq) | Salt-stress FPKM values and differential-expression results | Counted 18 responsive genes and plotted the time-course heatmap |
| Table S4 | The differentially expressed VcbZIP genes under drought stress from transcriptome sequencing (RNA-Seq) | Drought-stress FPKM values and differential-expression results | Counted 13 responsive genes and plotted the time-course heatmap |

The heatmaps use log10(mean FPKM + 1) across the three reported samples at each time point.

The official Draper V1.0 protein FASTA, GFF annotation, and scaffold FASTA have been downloaded and checked. They are ready for bZIP candidate identification.

A local homology screen using the 153 reference proteins extracted from the paper found 267 candidate proteins at E-value <= 1e-5 and recovered every paper reference protein. This is broader than the paper's final set because sequence similarity alone does not confirm the bZIP domain. Pfam, SMART, or CDD domain confirmation is the next required step.

Pfam-domain confirmation is complete. The 267 homology candidates were checked for the four bZIP domains used by the paper: PF00170, PF07716, PF03131, and PF12498. A total of 214 proteins contained at least one target domain. This set includes all 153 paper reference proteins and 61 additional domain-confirmed candidates. The paper's final 102 VcbZIP names combine homoeologous copies and remove duplicate or incomplete sequences, so the remaining filtering rules must be reconstructed before comparing a final count.

The available evidence does not support a deterministic final filter for the additional 61 proteins: none is an exact duplicate of a paper-reference protein, and only one is shorter than 100 amino acids. The paper does not publish a sequence-level exclusion list. This is a documented limitation of the from-scratch gene-identification reproduction.

Table S2 promoter statistics were also reproduced. The paper's 102 VcbZIP promoters contain 261 predicted abscisic-acid-responsive elements across 82 genes. This result currently comes from the supplied promoter table. The genome-derived promoter extraction and independent cis-element scan remain to be run.

Genome-derived promoter extraction is complete. The Draper GFF and genome FASTA produced 153 upstream sequences for the 102 VcbZIP names because several names represent multiple homoeologous copies. One VcbZIP43 copy has only 430 bp available before a scaffold boundary. The resulting promoter FASTA is ready for an independent PlantCARE batch scan; the scan itself remains pending because PlantCARE provides this analysis through its web interface rather than a stable public batch API.

An initial phylogenetic reconstruction is complete. The 153 blueberry protein copies from the paper were aligned with 78 canonical Arabidopsis bZIP reference proteins, excluding AtbZIP73 because it is a pseudogene. The local UPGMA tree contains 231 tips and maps each blueberry copy to its nearest Arabidopsis bZIP reference. This supports later group assignment but does not replace the paper's motif-based group classification.

Gene-structure analysis is complete from the Draper V1.0 GFF. Across 153 VcbZIP gene copies, exon counts range from 1 to 14. A total of 36 copies have one exon and 36 have four exons. The per-copy structure table is available for later comparison with the phylogenetic groups.

Conserved motif analysis is pending. The paper used MEME 4.10.1, which has no native Windows build; this computer has no WSL, Docker, or MEME executable. A substitute motif algorithm has not been used because it would no longer reproduce the paper's method.

## Planned Checkpoints

1. Run MEME motif discovery on a Linux-compatible environment and use it with the phylogeny for group assignment.
2. Compare gene structures across provisional phylogenetic branches.
3. Find a usable PlantCARE batch path or document the independent promoter-scan limitation.
3. Reproduce expression and differential analysis from public transcriptome data.
4. Compare results with the paper and document any differences.

