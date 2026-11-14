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

## 2026-11-14: genome-derived promoter extraction

- Goal: independently prepare the 2 kb upstream promoter sequences used as input for the paper's PlantCARE analysis.
- Environment: `D:\conda_envs\blueberry-bzip`, Python 3.11, Biopython.
- Command: `python scripts/extract_vcbzip_promoters.py --workbook <supplementary tables.xlsx> --gff <Draper GFF> --genome <Draper scaffold FASTA> --output-fasta <promoter FASTA> --output-table results/vcbzip-promoter-extraction.csv --length 2000`.
- Method: used the first CDS coordinate as the ATG position on plus-strand genes and the last CDS coordinate on minus-strand genes; minus-strand promoters were reverse complemented.
- Result: extracted 153 promoter sequences representing the paper's 102 VcbZIP names. One VcbZIP43 copy lies near a scaffold boundary and has only 430 bp upstream sequence.
- Output FASTA: `D:\science-data\datasets\feng-bzip-2025\reference\vcbzip-promoters-2kb.fasta`.
- Next: submit the promoter FASTA to PlantCARE through its web batch interface, then compare the downloaded `.tab` output against Table S2. PlantCARE has no stable public batch API for this script to call directly.

## 2026-11-14: preliminary phylogenetic analysis

- Goal: prepare the paper's phylogenetic-analysis input by combining blueberry VcbZIP proteins with the Arabidopsis bZIP reference set.
- Reference data: downloaded 78 canonical Arabidopsis bZIP proteins from Ensembl Plants using the published AtbZIP1-AtbZIP79 gene list, excluding pseudogene AtbZIP73.
- Environment: `D:\conda_envs\blueberry-bzip`, Python 3.11, Biopython, pyfamsa.
- Command: `python scripts/build_bzip_phylogeny.py --blueberry <VcbZIP reference FASTA> --arabidopsis <AtbZIP reference FASTA> --alignment results/bzip-blueberry-arabidopsis-alignment.fasta --tree results/bzip-upgma-tree.nwk --threads 8`.
- Result: aligned 153 blueberry protein copies and 78 Arabidopsis references, yielding 231 proteins across 2,172 alignment columns. Built a preliminary UPGMA tree and mapped every blueberry copy to its nearest Arabidopsis reference tip.
- Limitation: this tree is an initial similarity-based reconstruction. The paper's final A-S group labels also use conserved motif evidence and should not be assigned from nearest-neighbor relationships alone.
- Output: `results/bzip-blueberry-arabidopsis-alignment.fasta`, `results/bzip-upgma-tree.nwk`, and `results/bzip-nearest-arabidopsis-references.csv`.

## 2026-11-14: gene-structure analysis

- Goal: reproduce the exon-intron structure input from the Draper V1.0 GFF annotation.
- Environment: `D:\conda_envs\blueberry-bzip`, Python 3.11, pandas, Biopython, matplotlib.
- Command: `python scripts/summarize_vcbzip_gene_structures.py --workbook <supplementary tables.xlsx> --gff <Draper GFF> --output-dir results`.
- Result: summarized 153 gene copies across 102 VcbZIP names. Exon count ranges from 1 to 14. The most common exon counts are 1 and 4, each occurring in 36 gene copies.
- Output: `results/vcbzip-gene-structures.csv`, `results/vcbzip-exon-count-summary.csv`, and `results/figures/vcbzip-exon-counts.png`.

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
- Output: `configs/rna-seq-sample-manifest.csv`, `results/drought-fpkm-source-verification.csv`, and `results/salt-aba-source-membership-verification.csv`.

## 2026-11-13: documentation clarification

- Added explicit descriptions of supplementary Tables S1, S3, and S4 to the experiment summary and metrics table.
- This clarifies that S1 provides the identified VcbZIP list, S3 provides salt-stress RNA-seq results, and S4 provides drought-stress RNA-seq results.

## Next Run

- Inspect Supplementary Tables S1-S10.
- Map each table to the paper's figures and claims.
- Confirm the genome and annotation download links.
- Check BioProject sample metadata and run accessions.

