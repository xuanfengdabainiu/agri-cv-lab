# Genome-Wide Analysis of Blueberry bZIP Transcription Factors

## Goal

Reproduce the computational analysis of Feng et al. (2025) on bZIP transcription factors in blueberry and their expression responses to salt, drought, and ABA stress.

## Paper

- Title: Genome-Wide Analysis of bZIP Transcription Factors and Expression Patterns in Response to Salt and Drought Stress in *Vaccinium corymbosum*
- Authors: Xinghua Feng et al.
- Journal: International Journal of Molecular Sciences
- Year: 2025
- DOI: https://doi.org/10.3390/ijms26020843
- Zotero item key: `JUSWJ5C8`

## Status

`setup`

## Data Sources

- Blueberry genome and annotations: Genome Database for *Vaccinium* (Draper V1.0)
- Drought RNA-seq: `PRJNA1160404`
- Salt RNA-seq: `PRJNA1128395`
- ABA RNA-seq: `PRJNA997066`
- Supplementary materials: `D:\science-data\datasets\feng-bzip-2025\supplementary`

## Planned Scope

### Phase 1: lightweight reproduction

Use the supplementary tables and publicly available expression data to reproduce the reported gene counts, stress response lists, heatmap inputs, and selected correlations.

### Phase 2: genome-wide analysis

Rebuild the bZIP identification and annotation workflow using the blueberry genome, Pfam HMMs, Arabidopsis reference sequences, phylogenetic analysis, motif analysis, gene structures, and promoter cis-elements.

### Phase 3: raw RNA-seq reproduction

Download the SRA reads, run quality control and quantification, perform differential expression analysis with DESeq2, and compare the results with the paper.

## Local Storage

- Project records and scripts: this directory in `agri-cv-lab`
- Supplementary files and large datasets: `D:\science-data\datasets\feng-bzip-2025`
- Runs and intermediate outputs: `D:\science-data\runs\feng-bzip-2025`

## Reproduction Notes

The paper reports 102 VcbZIP genes. It uses Pfam bZIP domains, Arabidopsis sequences, the Vaccinium genome database, MEGA X, MEME, CDD, PlantCARE, TBtools-II, and DESeq2.

The raw salt and drought projects are large. The lightweight phase will be completed before downloading all raw FASTQ files.

