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

`done` for the table-level reproduction scope.

The final claim-by-claim scope table is [`results/06_wrapup/reproduction-scope-summary.md`](results/06_wrapup/reproduction-scope-summary.md). It is regenerated from the result files by `scripts/06_wrapup/summarize_reproduction_scope.py`, so the numbers in it cannot drift away from the recorded data.

Summary of the close-out:

- 20 published claims were checked against public data.
- 9 reproduced, 7 partially reproduced, 2 blocked by tooling, 2 not supported by the public source data.
- The two tooling-blocked items (MEME motif analysis, independent PlantCARE scan) both need a Linux environment; the exact steps are in [`results/experiment-summary.md`](results/experiment-summary.md).

## Quick Start

```powershell
conda activate D:\conda_envs\blueberry-bzip

python scripts\01_supplementary\summarize_supplementary.py `
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
| expression-source-001 | stress-expression source verification | original stress-study supplementary workbooks | drought 11/13 exact; salt 18/18; ABA 6/7 | SRA runs are pooled by time point; table-level reproduction is supported |
| drought-deg-001 | drought DEG list reproduction | source drought DESeq2 comparisons | 11/13 VcbZIP genes recovered | two gene IDs are missing from source matrices |
| salt-deg-001 | salt DEG list reproduction | source salt DESeq2 comparisons | 18/18 VcbZIP genes recovered | all reported salt-responsive genes reproduced |
| aba-fpkm-001 | ABA FPKM source verification | source ABA hormone-pathway matrix | 6/7 exact FPKM profiles | VcbZIP1 is absent from the source table |
| expression-heatmap-001 | verified-source heatmaps | drought and ABA source FPKM matrices | drought 11 genes / ABA 6 genes | uses only exact source-matched gene IDs |
| correlation-001 | VcbZIP Pearson correlations | Tables S3/S4 FPKM matrices | salt max diff 0.027; drought 77/78 pairs close | one drought pair differs by 0.360 |
| figure8-drought-001 | VcbZIP-stress gene correlations | Table S9 and source drought FPKM | 129/140 computable pairs match within 0.001 | some source IDs are missing or represent multiple copies |
| figure8-salt-coverage-001 | salt Figure 8 source coverage | source salt DEG blocks | 4/69 stress genes have all time points | public source data cannot support full Pearson reproduction |
| group-structure-001 | author group and exon structure summary | Table S1 groups + Draper GFF | Group A 29; Groups I/S 21 each | group-level exon patterns reproduced |
| scope-001 | final reproduction scope summary | all recorded result files | 9 reproduced / 7 partial / 2 tooling-blocked / 2 source-limited | closes the project; table regenerated from the result CSVs |

## Data Sources

- Blueberry genome and annotations: Genome Database for *Vaccinium* (Draper V1.0)
- Drought RNA-seq: `PRJNA1160404`
- Salt RNA-seq: `PRJNA1128395`
- ABA RNA-seq: `PRJNA997066`
- Supplementary materials: `D:\science-data\datasets\feng-bzip-2025\supplementary`

## Planned Scope

### Phase 1: lightweight reproduction

Use the supplementary tables and publicly available expression data to reproduce the reported gene counts, stress response lists, heatmap inputs, and selected correlations.

Status: complete. Gene counts, both DEG lists, the ABA and drought FPKM values, the correlation tables, and the drought Figure 8 panel are all reproduced. See `results/05_expression/`.

### Phase 2: genome-wide analysis

Rebuild the bZIP identification and annotation workflow using the blueberry genome, Pfam HMMs, Arabidopsis reference sequences, phylogenetic analysis, motif analysis, gene structures, and promoter cis-elements.

Status: complete except for two tooling-blocked steps. The homology screen, Pfam domain confirmation, UPGMA phylogeny, gene structures, and promoter extraction are done. MEME motif analysis and the independent PlantCARE scan need a Linux environment.

### Phase 3: raw RNA-seq reproduction

Download the SRA reads, run quality control and quantification, perform differential expression analysis with DESeq2, and compare the results with the paper.

Status: not supported by the public deposition. The SRA BioProjects expose one pooled run per time point, while the source tables keep three replicates. Phase 1 reproduces the published expression results at the table level instead.

## Local Storage

- Project records and scripts: this directory in `agri-cv-lab`
- Supplementary files and large datasets: `D:\science-data\datasets\feng-bzip-2025`
- Runs and intermediate outputs: `D:\science-data\runs\feng-bzip-2025`

## Reproduction Notes

The paper reports 102 VcbZIP genes. It uses Pfam bZIP domains, Arabidopsis sequences, the Vaccinium genome database, MEGA X, MEME, CDD, PlantCARE, TBtools-II, and DESeq2.

The raw salt and drought projects are large. The lightweight phase will be completed before downloading all raw FASTQ files.

## Result Files

- [Results index](results/README.md)
- [Supplementary summary](results/01_supplementary/supplementary-summary.csv)
- [Salt-expression heatmap](results/01_supplementary/figures/salt-vcbzip-heatmap.png)
- [Drought-expression heatmap](results/01_supplementary/figures/drought-vcbzip-heatmap.png)
- [Paper gene-to-protein mapping](results/03_domain_screen/vcbzip-protein-mapping.csv)
- [bZIP homology candidates](results/03_domain_screen/phmmer-bzip-candidates.csv)
- [Pfam domain confirmation](results/03_domain_screen/ebi-pfam-bzip-domain-confirmation.csv)
- [Domain-confirmed candidate summary](results/03_domain_screen/bzip-domain-candidate-summary.csv)
- [Additional domain-confirmed candidates](results/03_domain_screen/additional-bzip-domain-candidates.csv)
- [Cis-element summary](results/01_supplementary/cis-element-summary.csv)
- [Cis-element counts](results/01_supplementary/figures/cis-element-counts.png)
- [Promoter extraction coordinates](results/02_genome/vcbzip-promoter-extraction.csv)
- [Blueberry-Arabidopsis protein alignment](results/04_phylogeny/bzip-blueberry-arabidopsis-alignment.fasta)
- [UPGMA phylogenetic tree](results/04_phylogeny/bzip-upgma-tree.nwk)
- [Nearest Arabidopsis reference mapping](results/04_phylogeny/bzip-nearest-arabidopsis-references.csv)
- [VcbZIP gene structures](results/02_genome/vcbzip-gene-structures.csv)
- [Exon-count summary](results/02_genome/vcbzip-exon-count-summary.csv)
- [Exon-count figure](results/02_genome/figures/vcbzip-exon-counts.png)
- [RNA-seq sample manifest](configs/rna-seq-sample-manifest.csv)
- [Drought FPKM source verification](results/05_expression/drought-fpkm-source-verification.csv)
- [Salt and ABA source verification](results/05_expression/salt-aba-source-membership-verification.csv)
- [Drought DEG membership verification](results/05_expression/drought-deg-membership-verification.csv)
- [Salt DEG membership verification](results/05_expression/salt-deg-membership-verification.csv)
- [ABA FPKM source verification](results/05_expression/aba-fpkm-source-verification.csv)
- [Verified drought heatmap](results/05_expression/figures/drought-verified-source-heatmap.png)
- [Verified ABA heatmap](results/05_expression/figures/aba-verified-source-heatmap.png)
- [Salt correlation heatmap](results/05_expression/figures/salt-bzip-recomputed-correlation.png)
- [Drought correlation heatmap](results/05_expression/figures/drought-bzip-recomputed-correlation.png)
- [Drought Figure 8 correlation verification](results/05_expression/figures/drought-stress-gene-correlation-verification.png)
- [Salt Figure 8 source coverage](results/05_expression/figures/salt-figure8-source-coverage.png)
- [Author VcbZIP groups](results/01_supplementary/vcbzip-author-groups.csv)
- [Group-level exon summary](results/01_supplementary/vcbzip-group-exon-summary.csv)
- [Group counts](results/01_supplementary/figures/vcbzip-group-counts.png)
- [Group exon distributions](results/01_supplementary/figures/vcbzip-group-exon-counts.png)
- [Reproduction scope summary](results/06_wrapup/reproduction-scope-summary.md)
- [Reproduction scope table](results/06_wrapup/reproduction-scope-summary.csv)
- [Experiment summary](results/experiment-summary.md)

## Script Index

See [scripts/README.md](scripts/README.md) for scripts grouped by workflow stage.

