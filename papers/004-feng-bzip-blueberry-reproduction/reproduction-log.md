# Reproduction Log

## 2026-11-13

- Created the project record.
- Located the paper in Zotero (`JUSWJ5C8`).
- Confirmed the PDF is available locally.
- Identified the three NCBI BioProjects reported by the paper:
  - `PRJNA1160404` drought stress
  - `PRJNA1128395` salt stress
  - `PRJNA997066` ABA stress
- Downloaded the MDPI supplementary archive to `D:\science-data\datasets\feng-bzip-2025\supplementary`.
- Extracted `Figure S1.pdf` and `supplementary tables.xlsx`.
- No model training or raw RNA-seq processing has been run yet.

## 2026-11-13: supplementary-table summary

- Created the `blueberry-bzip` Conda environment at `D:\conda_envs\blueberry-bzip`.
- Added `scripts/summarize_supplementary.py` to summarize Tables S1, S3, and S4.
- Reproduced the three counts reported in the paper from the supplied workbook:
  - 102 VcbZIP genes in Table S1
  - 18 salt-responsive VcbZIP genes in Table S3
  - 13 drought-responsive VcbZIP genes in Table S4
- Calculated mean FPKM for each treatment time point across the three supplied replicate columns.
- Generated salt and drought expression heatmaps using log10(mean FPKM + 1).
- This step reproduces the supplementary-table summaries only. It does not rerun differential expression from raw RNA-seq reads.

## 2026-11-13: Draper V1.0 genome preparation

- Downloaded the official `Vaccinium corymbosum` cv. Draper V1.0 protein FASTA, GFF gene annotation, and scaffold FASTA from GDV.
- Stored files under `D:\science-data\datasets\feng-bzip-2025\genome`.
- Validated 128,559 protein sequences and 128,559 GFF gene features.
- Validated 1,760 scaffolds and 1,826,686,181 genome bases.
- These files are ready for the bZIP candidate-identification, gene-structure, and promoter-sequence stages.

## 2026-11-13: bZIP homology candidate screen

- Installed `pyhmmer` in the `blueberry-bzip` environment because a native HMMER command was not available on this Windows setup.
- Mapped the paper's 102 VcbZIP names to 153 unique Draper V1.0 protein records. Several VcbZIP names represent multiple homoeologous gene IDs.
- Used the 153 reference proteins to search all 128,559 proteins with local `phmmer` at E-value <= 1e-5.
- The union contained 267 candidate proteins and recovered all 153 paper reference proteins.
- The extra 114 proteins require bZIP-domain confirmation before they can be treated as final candidates. The paper used Pfam profiles plus SMART/CDD confirmation and manual filtering, so this homology screen is a preliminary candidate stage.

## Next Run

- Inspect Supplementary Tables S1-S10.
- Map each table to the paper's figures and claims.
- Confirm the genome and annotation download links.
- Check BioProject sample metadata and run accessions.

