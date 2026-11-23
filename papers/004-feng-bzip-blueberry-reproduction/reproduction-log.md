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
- Command: `python scripts/01_supplementary/summarize_supplementary.py --workbook <supplementary tables.xlsx> --output-dir results`.
- Created the `blueberry-bzip` Conda environment at `D:\conda_envs\blueberry-bzip`.
- Added `scripts/01_supplementary/summarize_supplementary.py` to summarize Tables S1, S3, and S4.
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
- Command: `python scripts/03_domain_screen/phmmer_bzip_candidates.py --references <reference FASTA> --proteins <Draper protein FASTA> --output results/03_domain_screen/phmmer-bzip-candidates.csv --cpus 8 --evalue 1e-5`.
- Installed `pyhmmer` in the `blueberry-bzip` environment because a native HMMER command was not available on this Windows setup.
- Mapped the paper's 102 VcbZIP names to 153 unique Draper V1.0 protein records. Several VcbZIP names represent multiple homoeologous gene IDs.
- Used the 153 reference proteins to search all 128,559 proteins with local `phmmer` at E-value <= 1e-5.
- The union contained 267 candidate proteins and recovered all 153 paper reference proteins.
- The extra 114 proteins require bZIP-domain confirmation before they can be treated as final candidates. The paper used Pfam profiles plus SMART/CDD confirmation and manual filtering, so this homology screen is a preliminary candidate stage.

## 2026-11-14: Pfam bZIP-domain confirmation

- Goal: confirm whether the 267 homology candidates contain one or more of the four bZIP Pfam domains reported in the paper: PF00170, PF07716, PF03131, and PF12498.
- Environment: `D:\conda_envs\blueberry-bzip`, Python 3.11, pyhmmer 0.12.3.
- Method: submitted candidate proteins one at a time to the EBI HMMER Pfam API with five concurrent requests. NCBI Batch CD-Search could not be used programmatically because it returned a CAPTCHA page.
- Command: `python scripts/03_domain_screen/confirm_bzip_domains_ebi.py --input <candidate FASTA> --output results/03_domain_screen/ebi-pfam-bzip-domain-confirmation.csv --workers 5`.
- Result: all 267 API jobs completed successfully. Of 267 homology candidates, 214 had at least one target bZIP Pfam domain. All 153 paper reference proteins were confirmed. The remaining 61 domain-confirmed proteins are additional candidates that need the paper's duplicate and completeness filtering rules.
- Output: `results/03_domain_screen/ebi-pfam-bzip-domain-confirmation.csv` and `results/03_domain_screen/bzip-domain-candidate-summary.csv`.

## 2026-11-14: candidate-filter review

- Goal: assess whether the paper's stated duplicate and incomplete-sequence filtering can explain the 61 domain-confirmed proteins outside the paper reference set.
- Result: none of the 61 additional candidates is an exact amino-acid duplicate of a paper reference protein. Only one is shorter than 100 amino acids; the remaining candidates have normal protein lengths and bZIP domain hits.
- Conclusion: the paper does not provide enough per-sequence filtering detail to reproduce the final reduction from 214 domain-confirmed proteins to 102 VcbZIP names automatically. This is recorded as a reproducibility limitation rather than resolved by an arbitrary filter.

## 2026-11-14: promoter cis-element supplementary-table summary

- Goal: reproduce the promoter cis-element statistics in Table S2.
- Environment: `D:\conda_envs\blueberry-bzip`, Python 3.11, pandas, openpyxl, matplotlib.
- Command: `python scripts/01_supplementary/summarize_cis_elements.py --workbook <supplementary tables.xlsx> --output-dir results`.
- Result: 82 of 102 VcbZIP promoters contain abscisic-acid-responsive elements, totaling 261 elements. The next most frequent categories are MeJA-responsive elements (135 elements across 79 genes) and gibberellin-responsive elements (92 across 57 genes).
- Output: `results/01_supplementary/cis-element-summary.csv` and `results/01_supplementary/figures/cis-element-counts.png`.

## 2026-11-14: genome-derived promoter extraction

- Goal: independently prepare the 2 kb upstream promoter sequences used as input for the paper's PlantCARE analysis.
- Environment: `D:\conda_envs\blueberry-bzip`, Python 3.11, Biopython.
- Command: `python scripts/02_genome/extract_vcbzip_promoters.py --workbook <supplementary tables.xlsx> --gff <Draper GFF> --genome <Draper scaffold FASTA> --output-fasta <promoter FASTA> --output-table results/02_genome/vcbzip-promoter-extraction.csv --length 2000`.
- Method: used the first CDS coordinate as the ATG position on plus-strand genes and the last CDS coordinate on minus-strand genes; minus-strand promoters were reverse complemented.
- Result: extracted 153 promoter sequences representing the paper's 102 VcbZIP names. One VcbZIP43 copy lies near a scaffold boundary and has only 430 bp upstream sequence.
- Output FASTA: `D:\science-data\datasets\feng-bzip-2025\reference\vcbzip-promoters-2kb.fasta`.
- Next: submit the promoter FASTA to PlantCARE through its web batch interface, then compare the downloaded `.tab` output against Table S2. PlantCARE has no stable public batch API for this script to call directly.

## 2026-11-14: preliminary phylogenetic analysis

- Goal: prepare the paper's phylogenetic-analysis input by combining blueberry VcbZIP proteins with the Arabidopsis bZIP reference set.
- Reference data: downloaded 78 canonical Arabidopsis bZIP proteins from Ensembl Plants using the published AtbZIP1-AtbZIP79 gene list, excluding pseudogene AtbZIP73.
- Environment: `D:\conda_envs\blueberry-bzip`, Python 3.11, Biopython, pyfamsa.
- Command: `python scripts/04_phylogeny/build_bzip_phylogeny.py --blueberry <VcbZIP reference FASTA> --arabidopsis <AtbZIP reference FASTA> --alignment results/04_phylogeny/bzip-blueberry-arabidopsis-alignment.fasta --tree results/04_phylogeny/bzip-upgma-tree.nwk --threads 8`.
- Result: aligned 153 blueberry protein copies and 78 Arabidopsis references, yielding 231 proteins across 2,172 alignment columns. Built a preliminary UPGMA tree and mapped every blueberry copy to its nearest Arabidopsis reference tip.
- Limitation: this tree is an initial similarity-based reconstruction. The paper's final A-S group labels also use conserved motif evidence and should not be assigned from nearest-neighbor relationships alone.
- Output: `results/04_phylogeny/bzip-blueberry-arabidopsis-alignment.fasta`, `results/04_phylogeny/bzip-upgma-tree.nwk`, and `results/04_phylogeny/bzip-nearest-arabidopsis-references.csv`.

## 2026-11-14: gene-structure analysis

- Goal: reproduce the exon-intron structure input from the Draper V1.0 GFF annotation.
- Environment: `D:\conda_envs\blueberry-bzip`, Python 3.11, pandas, Biopython, matplotlib.
- Command: `python scripts/02_genome/summarize_vcbzip_gene_structures.py --workbook <supplementary tables.xlsx> --gff <Draper GFF> --output-dir results`.
- Result: summarized 153 gene copies across 102 VcbZIP names. Exon count ranges from 1 to 14. The most common exon counts are 1 and 4, each occurring in 36 gene copies.
- Output: `results/02_genome/vcbzip-gene-structures.csv`, `results/02_genome/vcbzip-exon-count-summary.csv`, and `results/02_genome/figures/vcbzip-exon-counts.png`.

## 2026-11-14: motif-analysis environment check

- The paper used MEME 4.10.1 with a maximum of 10 motifs.
- MEME Suite has no native Windows build. This computer has no WSL, Docker, or native MEME executable.
- The motif analysis is pending a Linux/WSL/remote execution environment. It is not replaced with a different motif algorithm because that would not reproduce the paper's method.

## 2026-11-14: RNA-seq source-study metadata and supplementary-matrix verification

- Goal: verify the source datasets behind the bZIP paper's salt, drought, and ABA expression tables without downloading all raw FASTQ files.
- Downloaded NCBI SRA run metadata and supplementary archives from the three original stress studies.
- SRA metadata shows 5 drought runs (35.6 GB), 5 salt runs (37.9 GB), and 3 ABA runs (18.2 GB). Each run corresponds to one treatment time point.
- The original supplementary workbooks contain three FPKM or read-count replicates per time point. The SRA run sizes approximately equal the three replicate libraries combined, so the public raw runs cannot be separated back into the individual biological replicates.
- Drought verification: 11 of 13 VcbZIP entries have FPKM values that match the source matrix exactly across all 15 sample columns. Two bZIP-paper gene IDs are absent from the source matrix.
- Salt verification: all 18 salt-responsive VcbZIP genes appear in at least one source-study differential-expression comparison.
- ABA verification: 6 of 7 bZIP-paper ABA genes appear by identical gene ID in the source-study hormone-pathway table; VcbZIP1 is absent from that restricted table.
- Output: `configs/rna-seq-sample-manifest.csv`, `results/05_expression/drought-fpkm-source-verification.csv`, and `results/05_expression/salt-aba-source-membership-verification.csv`.

## 2026-11-14: drought DEG membership reproduction

- Goal: reproduce the bZIP paper's drought-responsive gene list using source drought-study DESeq2 result blocks.
- Command: `python scripts/05_expression/verify_drought_deg_membership.py --bzip-workbook <bZIP supplementary workbook> --source-workbook <drought supplementary workbook> --output results/05_expression/drought-deg-membership-verification.csv`.
- Method: checked P6_vs_P0, P12_vs_P0, P24_vs_P0, and P48_vs_P0 using absolute log2FC >= 1 and p < 0.05.
- Result: 11 of 13 VcbZIP genes are independently recovered. The two unresolved genes are the same two IDs absent from the original drought FPKM matrix.
- Output: `results/05_expression/drought-deg-membership-verification.csv`.

## 2026-11-14: salt DEG membership reproduction

- Goal: reproduce the bZIP paper's salt-responsive gene list using source salt-study DESeq2 result blocks.
- Command: `python scripts/05_expression/verify_salt_deg_membership.py --bzip-workbook <bZIP supplementary workbook> --source-workbook <salt supplementary workbook> --output results/05_expression/salt-deg-membership-verification.csv`.
- Method: checked S6_vs_S0, S12_vs_S0, S24_vs_S0, and S48_vs_S0 using absolute log2FC >= 1 and p < 0.05.
- Result: all 18 VcbZIP genes are independently recovered as salt responsive. The output also records the source-study time comparisons where each gene was significant.
- Output: `results/05_expression/salt-deg-membership-verification.csv`.

## 2026-11-15: ABA FPKM source verification

- Goal: compare the seven ABA-responsive VcbZIP expression profiles in the bZIP paper against the original ABA-study supplementary matrix.
- Command: `python scripts/05_expression/verify_aba_fpkm_source.py --bzip-workbook <bZIP supplementary workbook> --source-workbook <ABA supplementary workbook> --output results/05_expression/aba-fpkm-source-verification.csv`.
- Result: six of seven VcbZIP entries match all nine FPKM values exactly across 0 h, 6 h, and 12 h triplicates. VcbZIP1 is absent from the source ABA hormone-pathway table.
- Output: `results/05_expression/aba-fpkm-source-verification.csv`.

## 2026-11-15: verified source-expression heatmaps

- Goal: redraw bZIP drought and ABA heatmaps using original stress-study FPKM matrices rather than copied bZIP-paper tables.
- Command: `python scripts/05_expression/plot_verified_source_expression.py --mode <drought|aba> --bzip-workbook <bZIP supplementary workbook> --source-workbook <source workbook> --verification <verification CSV> --output-dir results/05_expression`.
- Result: created a drought heatmap for 11 source-verified VcbZIP genes and an ABA heatmap for 6 source-verified VcbZIP genes. For all included genes, source FPKM values match the bZIP paper values exactly.
- Output: `results/05_expression/drought-verified-source-mean-fpkm.csv`, `results/05_expression/aba-verified-source-mean-fpkm.csv`, and heatmaps in `results/05_expression/figures`.

## 2026-11-15: drought VcbZIP-stress gene correlation verification

- Goal: reproduce the drought VcbZIP-to-stress-responsive-gene Pearson correlations in Table S9 and Figure 8.
- Command: `python scripts/05_expression/verify_drought_stress_gene_correlations.py --bzip-workbook <bZIP supplementary workbook> --source-workbook <drought supplementary workbook> --output results/05_expression/drought-stress-gene-correlation-verification.csv`.
- Method: used three-replicate mean FPKM at P0/P6/P12/P24/P48. For Table S9 rows containing multiple slash-separated gene IDs, selected the source gene ID whose recomputed correlation was closest to the reported value.
- Result: 140 of 162 reported correlations were computable from source matrices; 129 matched within 0.001. The other 22 use bZIP IDs missing from the source matrix. A small number of computable correlations differ more substantially, likely due to ambiguous multi-copy gene rows.
- Output: `results/05_expression/drought-stress-gene-correlation-verification.csv` and `results/05_expression/figures/drought-stress-gene-correlation-verification.png`.

## 2026-11-15: salt Figure 8 source-coverage assessment

- Goal: determine whether the public salt-study DEG read-count blocks contain enough timepoint coverage to independently reproduce the salt VcbZIP-stress-gene correlations in Table S8.
- Command: `python scripts/05_expression/assess_salt_figure8_coverage.py --bzip-workbook <bZIP supplementary workbook> --source-workbook <salt supplementary workbook> --output-dir results/05_expression`.
- Result: of 69 stress-responsive genes in Table S8, only 4 have read counts available in all four salt-treatment comparison blocks. The remaining genes lack one or more timepoints because the public source table only retains genes significant in each individual comparison.
- Conclusion: the public salt source does not contain a complete expression matrix for Table S8 genes, so a source-level Pearson reproduction would be unreliable and was not performed.
- Output: `results/05_expression/salt-figure8-source-coverage.csv`, `results/05_expression/salt-figure8-source-coverage-summary.csv`, and `results/05_expression/figures/salt-figure8-source-coverage.png`.

## 2026-11-15: author group and gene-structure summary

- Goal: recover the Table S1 VcbZIP group assignments and relate them to GFF-derived exon structure.
- Command: `python scripts/01_supplementary/summarize_vcbzip_groups.py --workbook <supplementary tables.xlsx> --gene-structures results/02_genome/vcbzip-gene-structures.csv --output-dir results/01_supplementary`.
- Method: forward-filled Excel merged group labels in Table S1, then merged author groups with the 153-copy gene-structure table.
- Result: Group A has 29 VcbZIP names, Groups I and S have 21 each. Group S has a median of one exon per copy, while Groups D and G have higher exon counts. This supports the paper's observation that gene structures differ across phylogenetic groups.
- Output: group assignment, group summary, group-level exon summary, and two figures in `results/01_supplementary`.

## 2026-11-15: VcbZIP correlation-table reproduction

- Goal: reproduce the Pearson correlation coefficients in Tables S6 (salt) and S7 (drought).
- Method: calculated mean FPKM across the three repeats at each time point, then calculated Pearson r across the five treatment time points for every VcbZIP pair.
- Command: `python scripts/05_expression/reproduce_bzip_correlations.py --workbook <bZIP supplementary workbook> --mode <salt|drought> --output-dir results/05_expression`.
- Result: salt correlations reproduce the paper closely across all 153 gene pairs, with maximum absolute difference 0.027. Drought correlations reproduce 77 of 78 pairs closely; VcbZIP83-VcbZIP45 differs by 0.360, while all other pairwise differences are <= 0.019.
- Output: recomputed matrices, pairwise comparison tables, and heatmaps in `results/05_expression`.

## 2026-11-14: script organization

- Grouped project scripts into `01_supplementary`, `02_genome`, `03_domain_screen`, `04_phylogeny`, and `05_expression`.
- Added `scripts/README.md` as an index describing the purpose of each script.
- Updated recorded command paths and the README quick-start command.

## 2026-11-14: result organization

- Grouped result files into `01_supplementary`, `02_genome`, `03_domain_screen`, `04_phylogeny`, and `05_expression`.
- Kept `metrics.md` and `experiment-summary.md` in the results root as project-level overview files.
- Added `results/README.md` as a result index and updated README links and recorded output paths.

## 2026-11-13: documentation clarification

- Added explicit descriptions of supplementary Tables S1, S3, and S4 to the experiment summary and metrics table.
- This clarifies that S1 provides the identified VcbZIP list, S3 provides salt-stress RNA-seq results, and S4 provides drought-stress RNA-seq results.

## 2026-11-23: reproduction scope summary

- Goal: close the project by turning every recorded result file into one claim-by-claim scope table, and by recording the three remaining gaps with the exact steps that would close them.
- Method: added `scripts/06_wrapup/summarize_reproduction_scope.py`, which reads the recorded result CSVs and recomputes every reported number from those files, so the summary cannot drift away from the data.
- Command: `D:\conda_envs\blueberry-bzip\python.exe scripts\06_wrapup\summarize_reproduction_scope.py --results-dir results --output-dir results\06_wrapup`.
- Output: `results/06_wrapup/reproduction-scope-summary.md` and `results/06_wrapup/reproduction-scope-summary.csv`.
- Result: 20 checked claims. 9 reproduced, 7 partially reproduced, 2 blocked by tooling, 2 not supported by the public source data.
- Problem found and fixed during the run: `paper_vcbzip_name` stores four names twice in one cell (`VcbZIP16;VcbZIP16`, `VcbZIP84;VcbZIP84`, `VcbZIP90;VcbZIP90`, `VcbZIP97;VcbZIP97`). Counting unique values directly gave 106 names instead of 102. The script now splits these cells on `;`, which returns exactly 102.
- Environment check: the bioconda `meme` package (5.5.9) publishes `linux-64` and `macOS-64` only, so the MEME stage needs WSL and cannot run natively on this Windows machine. The PlantCARE web service still has no reachable batch endpoint from this machine, so the independent promoter scan is limited to a manual upload.
- Next step: finish the WSL 2 installation, then run MEME inside it and use `fimo` or the PlantCARE batch page on the 153 extracted promoters.

## 2026-11-23: project close-out and documentation

- Goal: make the closed state visible from every entry point so the project can be reported without re-reading all logs.
- Updated `results/experiment-summary.md`: added a one-line conclusion, the final status, the full claim table, a "Remaining Gaps and How to Close Them" section, an explicit limitations list, and a conclusion. The stage-by-stage notes are kept unchanged.
- Updated `README.md`: status moved from `setup` to `done`, phase statuses recorded, and the scope summary added to the result links.
- Updated `results/metrics.md`: the stale "setup stage" note was replaced, the analysis-oriented column set is now explained, and the `scope-001` row was added.
- Updated `scripts/README.md`: the index was missing 10 scripts that already existed, and the new `06_wrapup` stage is now listed with a run command.
- Updated `results/README.md`: replaced the descriptive index with a complete file list per stage, including `06_wrapup`.
- Updated `docs/experiment-index.md`: the 004 row now records `done` and its best result, and the previously unregistered `003` scaffold row was added.
- No new analysis was run in this step; only documentation and the scope-table script were changed.

## Next Run

- Finish the WSL 2 install on `D:\wsl\Ubuntu-24.04`, then create a `meme` conda environment inside it.
- Run `mememe` on the confirmed candidate proteins and compare the recovered motifs against the author group labels in `results/01_supplementary/vcbzip-author-groups.csv`.
- Scan the 153 promoter sequences in `D:\science-data\datasets\feng-bzip-2025\reference\vcbzip-promoters-2kb.fasta` with PlantCARE, either through the web batch page or with `fimo` and the PlantCARE matrices.
- If the advisor wants a new independent project, the 003 CitDet citrus detection folder is an empty scaffold and can be filled from the shared template.

