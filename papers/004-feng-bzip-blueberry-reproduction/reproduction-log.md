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

## Next Run

- Inspect Supplementary Tables S1-S10.
- Map each table to the paper's figures and claims.
- Confirm the genome and annotation download links.
- Check BioProject sample metadata and run accessions.

