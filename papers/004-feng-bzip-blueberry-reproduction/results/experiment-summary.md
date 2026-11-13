# Experiment Summary

## Current Status

The project has completed paper and data source inspection. The supplementary archive is available locally.

The first supplementary-table reproduction is complete. Tables S1, S3, and S4 reproduce the paper's reported counts of 102 VcbZIP genes, 18 salt-responsive VcbZIP genes, and 13 drought-responsive VcbZIP genes. Heatmaps use log10(mean FPKM + 1) across the three reported samples at each time point.

The official Draper V1.0 protein FASTA, GFF annotation, and scaffold FASTA have been downloaded and checked. They are ready for bZIP candidate identification.

A local homology screen using the 153 reference proteins extracted from the paper found 267 candidate proteins at E-value <= 1e-5 and recovered every paper reference protein. This is broader than the paper's final set because sequence similarity alone does not confirm the bZIP domain. Pfam, SMART, or CDD domain confirmation is the next required step.

## Planned Checkpoints

1. Confirm bZIP domains in the 267 homology candidates.
2. Rebuild the bZIP identification workflow.
3. Reproduce expression and differential analysis from public transcriptome data.
4. Compare results with the paper and document any differences.

