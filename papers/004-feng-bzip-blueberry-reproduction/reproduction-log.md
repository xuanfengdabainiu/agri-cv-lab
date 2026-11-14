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

- Goal: reproduce the paper's reported VcbZIP, salt-response, and drought-response counts from supplied tables.
- Environment: `D:\conda_envs\blueberry-bzip`, Python 3.11, pandas, openpyxl, matplotlib, seaborn.
- Command: `python scripts/summarize_supplementary.py --workbook <supplementary tables.xlsx> --output-dir results`.
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

- Goal: download and validate the exact Draper V1.0 files used by the paper.
- Output: `D:\science-data\datasets\feng-bzip-2025\genome`.
- Downloaded the official `Vaccinium corymbosum` cv. Draper V1.0 protein FASTA, GFF gene annotation, and scaffold FASTA from GDV.
- Stored files under `D:\science-data\datasets\feng-bzip-2025\genome`.
- Validated 128,559 protein sequences and 128,559 GFF gene features.
- Validated 1,760 scaffolds and 1,826,686,181 genome bases.
- These files are ready for the bZIP candidate-identification, gene-structure, and promoter-sequence stages.

## 2026-11-13: bZIP homology candidate screen

- Goal: use the paper's confirmed proteins as reference queries against the full Draper proteome.
- Environment: `D:\conda_envs\blueberry-bzip`, Python 3.11, pyhmmer 0.12.3.
- Command: `python scripts/phmmer_bzip_candidates.py --references <reference FASTA> --proteins <Draper protein FASTA> --output results/phmmer-bzip-candidates.csv --cpus 8 --evalue 1e-5`.
- Installed `pyhmmer` in the `blueberry-bzip` environment because a native HMMER command was not available on this Windows setup.
- Mapped the paper's 102 VcbZIP names to 153 unique Draper V1.0 protein records. Several VcbZIP names represent multiple homoeologous gene IDs.
- Used the 153 reference proteins to search all 128,559 proteins with local `phmmer` at E-value <= 1e-5.
- The union contained 267 candidate proteins and recovered all 153 paper reference proteins.
- The extra 114 proteins require bZIP-domain confirmation before they can be treated as final candidates. The paper used Pfam profiles plus SMART/CDD confirmation and manual filtering, so this homology screen is a preliminary candidate stage.

## 2026-11-14: Pfam bZIP-domain confirmation

- Goal: confirm whether the 267 homology candidates contain one or more of the four bZIP Pfam domains reported in the paper: PF00170, PF07716, PF03131, and PF12498.
- Environment: `D:\conda_envs\blueberry-bzip`, Python 3.11, pyhmmer 0.12.3.
- Method: submitted candidate proteins one at a time to the EBI HMMER Pfam API with five concurrent requests. NCBI Batch CD-Search could not be used programmatically because it returned a CAPTCHA page.
- Command: `python scripts/confirm_bzip_domains_ebi.py --input <candidate FASTA> --output results/ebi-pfam-bzip-domain-confirmation.csv --workers 5`.
- Result: all 267 API jobs completed successfully. Of 267 homology candidates, 214 had at least one target bZIP Pfam domain. All 153 paper reference proteins were confirmed. The remaining 61 domain-confirmed proteins are additional candidates that need the paper's duplicate and completeness filtering rules.
- Output: `results/ebi-pfam-bzip-domain-confirmation.csv` and `results/bzip-domain-candidate-summary.csv`.

## 2026-11-14: candidate-filter review

- Goal: assess whether the paper's stated duplicate and incomplete-sequence filtering can explain the 61 domain-confirmed proteins outside the paper reference set.
- Result: none of the 61 additional candidates is an exact amino-acid duplicate of a paper reference protein. Only one is shorter than 100 amino acids; the remaining candidates have normal protein lengths and bZIP domain hits.
- Conclusion: the paper does not provide enough per-sequence filtering detail to reproduce the final reduction from 214 domain-confirmed proteins to 102 VcbZIP names automatically. This is recorded as a reproducibility limitation rather than resolved by an arbitrary filter.

## 2026-11-14: promoter cis-element supplementary-table summary

- Goal: reproduce the promoter cis-element statistics in Table S2.
- Environment: `D:\conda_envs\blueberry-bzip`, Python 3.11, pandas, openpyxl, matplotlib.
- Command: `python scripts/summarize_cis_elements.py --workbook <supplementary tables.xlsx> --output-dir results`.
- Result: 82 of 102 VcbZIP promoters contain abscisic-acid-responsive elements, totaling 261 elements. The next most frequent categories are MeJA-responsive elements (135 elements across 79 genes) and gibberellin-responsive elements (92 across 57 genes).
- Output: `results/cis-element-summary.csv` and `results/figures/cis-element-counts.png`.

## 2026-11-13: documentation clarification

- Added explicit descriptions of supplementary Tables S1, S3, and S4 to the experiment summary and metrics table.
- This clarifies that S1 provides the identified VcbZIP list, S3 provides salt-stress RNA-seq results, and S4 provides drought-stress RNA-seq results.

## Next Run

- Inspect Supplementary Tables S1-S10.
- Map each table to the paper's figures and claims.
- Confirm the genome and annotation download links.
- Check BioProject sample metadata and run accessions.

