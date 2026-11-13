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

## Planned Checkpoints

1. Confirm bZIP domains in the 267 homology candidates.
2. Rebuild the bZIP identification workflow.
3. Reproduce expression and differential analysis from public transcriptome data.
4. Compare results with the paper and document any differences.

