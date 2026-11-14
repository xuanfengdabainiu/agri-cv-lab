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

## Quick Start

```powershell
conda activate D:\conda_envs\blueberry-bzip

python scripts\summarize_supplementary.py `
  --workbook "D:\science-data\datasets\feng-bzip-2025\supplementary\extracted\supplementary tables.xlsx" `
  --output-dir results
```

## Main Results

| Run | Analysis | Input | Result | Notes |
|---|---|---|---|---|
| supplementary-001 | Tables S1, S3, S4 summary | Supplementary workbook | 102 / 18 / 13 | Matches the paper's reported bZIP, salt-response, and drought-response counts |
| genome-001 | Draper V1.0 preparation | Protein FASTA, GFF, scaffold FASTA | 128,559 proteins / 1,760 scaffolds | File-level counts passed |
| candidate-001 | bZIP homology screen | 153 paper reference proteins | 267 candidates | All 153 reference proteins were recovered; domain confirmation is pending |
| domain-001 | Pfam bZIP-domain confirmation | 267 homology candidates | 214 domain-confirmed proteins | All 153 paper reference proteins confirmed; 61 extra candidates remain for duplicate/completeness filtering |
| cis-element-001 | promoter cis-element summary | Table S2 | 261 ABA-responsive elements across 82 genes | Genome-derived promoter analysis is pending |
| promoter-001 | genome-derived promoter extraction | Draper V1.0 GFF and scaffold FASTA | 153 sequences for 102 VcbZIP names | ready for PlantCARE batch analysis |
| phylogeny-001 | preliminary UPGMA tree | 153 VcbZIP copies + 78 AtbZIP references | 231 proteins / 2,172 columns | final group labels need motif evidence |
| structure-001 | exon-intron structure summary | Draper V1.0 GFF | 153 gene copies / exon range 1-14 | motif analysis requires a Linux-compatible MEME environment |

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

## Result Files

- [Supplementary summary](results/supplementary-summary.csv)
- [Salt-expression heatmap](results/figures/salt-vcbzip-heatmap.png)
- [Drought-expression heatmap](results/figures/drought-vcbzip-heatmap.png)
- [Paper gene-to-protein mapping](results/vcbzip-protein-mapping.csv)
- [bZIP homology candidates](results/phmmer-bzip-candidates.csv)
- [Pfam domain confirmation](results/ebi-pfam-bzip-domain-confirmation.csv)
- [Domain-confirmed candidate summary](results/bzip-domain-candidate-summary.csv)
- [Additional domain-confirmed candidates](results/additional-bzip-domain-candidates.csv)
- [Cis-element summary](results/cis-element-summary.csv)
- [Cis-element counts](results/figures/cis-element-counts.png)
- [Promoter extraction coordinates](results/vcbzip-promoter-extraction.csv)
- [Blueberry-Arabidopsis protein alignment](results/bzip-blueberry-arabidopsis-alignment.fasta)
- [UPGMA phylogenetic tree](results/bzip-upgma-tree.nwk)
- [Nearest Arabidopsis reference mapping](results/bzip-nearest-arabidopsis-references.csv)
- [VcbZIP gene structures](results/vcbzip-gene-structures.csv)
- [Exon-count summary](results/vcbzip-exon-count-summary.csv)
- [Exon-count figure](results/figures/vcbzip-exon-counts.png)
- [Experiment summary](results/experiment-summary.md)

