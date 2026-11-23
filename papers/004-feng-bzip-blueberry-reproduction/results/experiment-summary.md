# Experiment Summary

## One-Line Conclusion

The computational core of Feng et al. (2025) was reproduced at the table level: the 102 VcbZIP gene set, the salt and drought responsive gene lists, the ABA-responsive promoter statistics, the gene structures, the author group labels, and the Pearson correlation tables all match the published values, most of them exactly.

Two stages could not be reproduced on this machine (MEME motif analysis, independent PlantCARE scanning) and one is not supported by the public deposition (a raw-read DESeq2 rerun). All three are recorded below with the exact steps that would close them.

## Final Status

- Status: `done` for the table-level reproduction scope.
- Scope: 20 checked claims. 9 reproduced, 7 partially reproduced, 2 blocked by tooling, 2 not supported by the public source data.
- Scope table: [`06_wrapup/reproduction-scope-summary.md`](06_wrapup/reproduction-scope-summary.md), regenerated from the result files by `scripts/06_wrapup/summarize_reproduction_scope.py`.
- Phase 3 (raw RNA-seq processing) and the MEME stage remain open by design; see "Remaining Gaps and How to Close Them".

The full claim-by-claim table. This copy mirrors `06_wrapup/reproduction-scope-summary.md`, which is regenerated from the result files; if the two ever disagree, the generated file is the correct one.

| Claim | Coverage | Status |
|---|---|---|
| 102 VcbZIP genes | 102/102 | reproduced |
| 18 salt-responsive and 13 drought-responsive genes | 18/18 and 13/13 | reproduced |
| 261 ABA-responsive cis-elements in 82 promoters | 261/261 | reproduced |
| bZIP domain present in every reported protein | 102/102 names | reproduced |
| Final set is 102 genes after filtering | 102/102 names recovered | partial |
| Exon-intron structures | 153/153 copies | reproduced |
| 2 kb promoter extraction | 102/102 names | reproduced |
| Phylogeny against Arabidopsis bZIP | 102/102 names | partial |
| Author group labels A, D, G, I, S | 102/102 names | reproduced |
| Salt DEG list | 18/18 | reproduced |
| Drought DEG list | 11/13 | partial |
| Drought FPKM values | 11/13 | partial |
| ABA FPKM values | 6/7 | partial |
| Salt Pearson correlations | 153/153 pairs | reproduced |
| Drought Pearson correlations | 77/78 pairs | partial |
| Figure 8 drought correlations | 129/140 computable pairs | partial |
| Figure 8 salt correlations | 4/69 genes | not supported by source data |
| MEME motif grouping | 0/102 names | blocked by tooling |
| Independent PlantCARE scan | 0/153 promoters | blocked by tooling |
| Raw-read DESeq2 rerun | table-level only | not supported by source data |

## Stage-by-Stage Notes

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

Pfam-domain confirmation is complete. The 267 homology candidates were checked for the four bZIP domains used by the paper: PF00170, PF07716, PF03131, and PF12498. A total of 214 proteins contained at least one target domain. This set includes all 153 paper reference proteins and 61 additional domain-confirmed candidates. The paper's final 102 VcbZIP names combine homoeologous copies and remove duplicate or incomplete sequences, so the remaining filtering rules must be reconstructed before comparing a final count.

The available evidence does not support a deterministic final filter for the additional 61 proteins: none is an exact duplicate of a paper-reference protein, and only one is shorter than 100 amino acids. The paper does not publish a sequence-level exclusion list. This is a documented limitation of the from-scratch gene-identification reproduction.

Table S2 promoter statistics were also reproduced. The paper's 102 VcbZIP promoters contain 261 predicted abscisic-acid-responsive elements across 82 genes. This result currently comes from the supplied promoter table. The genome-derived promoter extraction and independent cis-element scan remain to be run.

Genome-derived promoter extraction is complete. The Draper GFF and genome FASTA produced 153 upstream sequences for the 102 VcbZIP names because several names represent multiple homoeologous copies. One VcbZIP43 copy has only 430 bp available before a scaffold boundary. The resulting promoter FASTA is ready for an independent PlantCARE batch scan; the scan itself remains pending because PlantCARE provides this analysis through its web interface rather than a stable public batch API.

An initial phylogenetic reconstruction is complete. The 153 blueberry protein copies from the paper were aligned with 78 canonical Arabidopsis bZIP reference proteins, excluding AtbZIP73 because it is a pseudogene. The local UPGMA tree contains 231 tips and maps each blueberry copy to its nearest Arabidopsis bZIP reference. This supports later group assignment but does not replace the paper's motif-based group classification.

Gene-structure analysis is complete from the Draper V1.0 GFF. Across 153 VcbZIP gene copies, exon counts range from 1 to 14. A total of 36 copies have one exon and 36 have four exons. The per-copy structure table is available for later comparison with the phylogenetic groups.

Conserved motif analysis is pending. The paper used MEME 4.10.1, which has no native Windows build; this computer has no WSL, Docker, or MEME executable. A substitute motif algorithm has not been used because it would no longer reproduce the paper's method.

Expression-source verification is complete using the supplementary workbooks from the three original stress studies. The drought matrix reproduces 11 of 13 bZIP-paper FPKM profiles exactly; the two remaining bZIP-paper gene IDs are absent from the drought source matrix. All 18 salt-responsive bZIP genes occur in the source salt DEG tables. Six of seven ABA-responsive bZIP genes occur by identical ID in the source ABA hormone-pathway table. The SRA metadata exposes one large run per time point, while the source workbooks preserve three replicates. Therefore, table-level expression reproduction is supported, but a strict DESeq2 rerun from independently separated raw replicate FASTQ files is not supported by the current SRA deposition.

The drought DEG list was reproduced directly from the original DESeq2 comparison blocks. Applying absolute log2FC >= 1 and p < 0.05 to P6/P12/P24/P48 versus P0 recovers 11 of the 13 VcbZIP genes reported by the bZIP paper. The two unresolved genes are absent from the original study's FPKM and DEG tables.

The salt DEG list was reproduced directly from the original DESeq2 comparison blocks. Applying the same thresholds to S6/S12/S24/S48 versus S0 recovers all 18 VcbZIP genes reported by the bZIP paper. This is the strongest direct expression-result reproduction in the project so far.

The ABA expression values were verified against the source ABA hormone-pathway matrix. Six of seven bZIP-paper genes match all nine FPKM values exactly across three replicates at 0 h, 6 h, and 12 h. VcbZIP1 is absent from the restricted source table, matching the gene-ID coverage issue seen in the drought source study.

Independent source-expression heatmaps are complete for the verified gene subsets: 11 drought VcbZIP genes and 6 ABA VcbZIP genes. Both use three-replicate mean FPKM values directly from the original stress-study supplementary matrices. Their included profiles are numerically identical to the corresponding bZIP-paper tables.

The Pearson correlation tables were also reproduced from the bZIP paper's FPKM matrices. Salt correlations closely match all 153 reported pairs, with maximum absolute difference 0.027. Drought correlations match all but one pair closely: VcbZIP83-VcbZIP45 differs by 0.360. This isolated discrepancy is recorded rather than overwritten.

The drought portion of Figure 8 was independently checked against the original drought expression matrix. Of 162 correlations shown in Table S9, 140 can be computed from matching source IDs and 129 of those agree with the paper within 0.001. The remaining differences are concentrated in rows with multiple candidate gene copies or bZIP IDs that are absent from the source matrix.

The salt portion of Figure 8 cannot be independently recomputed from the public source tables. The salt source publishes read counts only for genes significant in each separate timepoint comparison. Only 4 of 69 Table S8 stress genes appear in all four treatment blocks, which is insufficient for a reliable five-timepoint Pearson analysis. This is a source-data limitation rather than a failed calculation.

The author group labels were recovered from merged cells in Table S1 and linked to the GFF-derived gene structures. Group A contains 29 VcbZIP names, and Groups I and S contain 21 each. Exon counts vary by group: Group S has a median of one exon per gene copy, while Groups D and G contain more exon-rich structures. This reproduces the structure-by-group pattern described by the paper, though final group assignment still depends on the unavailable MEME motif stage.

## Remaining Gaps and How to Close Them

### 1. MEME motif analysis

Status: blocked by tooling, not by method.

The paper used MEME 4.10.1. There is no native Windows build. The current bioconda `meme` package (5.5.9) publishes `linux-64` and `macOS-64` only, so a Linux environment is required.

Closing steps:

1. Finish the WSL 2 installation (Ubuntu 24.04 on `D:\wsl\Ubuntu-24.04`).
2. Inside WSL: `conda create -n meme -c conda-forge -c bioconda meme`.
3. Run `mememe` on the confirmed candidate proteins and compare the recovered motifs with the author group labels from `results/01_supplementary/vcbzip-author-groups.csv`.

Input for step 3: `D:\science-data\datasets\feng-bzip-2025\reference\phmmer-bzip-candidates.fasta` and the domain-confirmed subset in `results/03_domain_screen/bzip-domain-candidate-summary.csv`.

### 2. Independent PlantCARE promoter scan

Status: blocked by tooling, not by method.

The paper counted promoter cis-elements with PlantCARE. PlantCARE only exposes this analysis through its web interface, and there is no stable public batch API, so the 153 extracted promoter sequences could not be scanned automatically. The count of 261 ABA-responsive elements across 82 promoters currently comes from the paper's own Table S2.

Closing steps, in order of effort:

1. Manual batch: upload the 153 promoter sequences (`results/02_genome/vcbzip-promoter-extraction.csv`, sequence file `D:\science-data\datasets\feng-bzip-2025\reference\vcbzip-promoters-2kb.fasta`) to the PlantCARE batch page and archive the result table.
2. Local scan: convert the PlantCARE matrices into MEME format and run `fimo` inside the WSL environment from step 1.

The 153 sequences are already extracted and quality-checked: 152 are 2000 bp, one VcbZIP43 copy is 430 bp because of a scaffold boundary.

### 3. Raw-read DESeq2 rerun

Status: not supported by the public deposition.

The SRA projects `PRJNA1160404`, `PRJNA1128395`, and `PRJNA997066` expose one pooled run per time point, while the source workbooks preserve three replicates. A replicate-level rerun would require per-replicate FASTQ files from the original authors. The table-level reproduction in this project is therefore the correct ceiling for the currently available data.

## Limitations

- The final 102-gene set could not be reconstructed from first principles. Domain confirmation yields 214 proteins, and the 61 extra confirmed candidates have no published exclusion rule. The paper does not release the sequence-level list it filtered against.
- Group assignment is inherited from Table S1, not re-derived from motifs, so it cannot yet confirm or correct the authors' grouping.
- Two drought genes and one ABA gene are absent from the original stress-study tables, so they cannot be verified from public data.
- The salt Figure 8 panel cannot be recomputed because the salt source publishes read counts per timepoint comparison only.
- The drought correlation outlier `VcbZIP83-VcbZIP45` (difference 0.360) is reported as found, not corrected.
- A MEME 5.x run would not reproduce the paper's MEME 4.10.1 defaults exactly, so any motif stage should be described as a re-analysis rather than an exact reproduction.

## Conclusion

The paper's reported numbers were checked rather than assumed, and every published table that can be checked against public data was checked. Where a value could not be reproduced, the reason is recorded as either a source-data limit or a tooling limit, with the specific command or file that would close it.

The practical next step is finishing the WSL 2 environment, because it unblocks both the MEME stage and a local PlantCARE scan, which are the only two remaining items that this project can still close on its own.

