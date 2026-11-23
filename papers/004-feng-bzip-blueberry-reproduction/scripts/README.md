# Scripts

Scripts are grouped by their place in the reproduction workflow.

## 01_supplementary

- `summarize_supplementary.py`: Summarizes Tables S1, S3, and S4 and draws expression heatmaps.
- `summarize_cis_elements.py`: Summarizes promoter cis-element counts from Table S2.
- `summarize_vcbzip_groups.py`: Recovers the author group labels from Table S1 and summarizes exon structure per group.

## 02_genome

- `extract_vcbzip_promoters.py`: Extracts 2 kb upstream promoter sequences from the Draper genome and GFF.
- `summarize_vcbzip_gene_structures.py`: Summarizes exon, intron, and gene-span structure from the GFF.

## 03_domain_screen

- `map_vcbzip_sequences.py`: Maps paper VcbZIP gene IDs to Draper proteins.
- `extract_vcbzip_reference_fasta.py`: Extracts paper-reference proteins from the Draper proteome.
- `phmmer_bzip_trial.py`: Runs one homology-search test.
- `phmmer_bzip_candidates.py`: Builds the union of bZIP-like homology candidates.
- `extract_candidate_fasta.py`: Extracts candidate protein sequences.
- `confirm_bzip_domains_ebi.py`: Confirms target bZIP Pfam domains with the EBI HMMER API.
- `summarize_domain_confirmation.py`: Combines domain hits with paper-reference membership.
- `analyze_bzip_candidates.py`: Summarizes protein lengths and possible incomplete candidates.
- `analyze_extra_bzip_candidates.py`: Examines additional domain-confirmed proteins.

## 04_phylogeny

- `download_arabidopsis_bzip_references.py`: Downloads the 78 Arabidopsis bZIP reference proteins.
- `build_bzip_phylogeny.py`: Builds the multiple alignment and initial UPGMA tree.
- `summarize_phylogeny_neighbors.py`: Finds the nearest Arabidopsis reference for each blueberry protein.

## 05_expression

- `summarize_sra_metadata.py`: Creates a concise sample manifest from NCBI SRA run metadata.
- `verify_drought_fpkm_source.py`: Compares Table S4 drought FPKM values with the source-study matrix.
- `verify_stress_source_membership.py`: Checks salt and ABA bZIP lists against source-study tables.
- `verify_aba_fpkm_source.py`: Verifies bZIP ABA FPKM values against the source ABA-study workbook.
- `verify_drought_deg_membership.py`: Verifies drought-responsive VcbZIP genes against the source DESeq2 blocks.
- `verify_salt_deg_membership.py`: Verifies salt-responsive VcbZIP genes against the source DESeq2 blocks.
- `reproduce_bzip_correlations.py`: Recomputes the Table S3 and S4 Pearson correlation matrices.
- `plot_bzip_correlations.py`: Plots the recomputed salt and drought correlation heatmaps.
- `verify_drought_stress_gene_correlations.py`: Checks the Table S9 VcbZIP-stress gene correlations against source drought FPKM.
- `plot_correlation_verification.py`: Plots reported versus recomputed correlation coefficients.
- `assess_salt_figure8_coverage.py`: Measures whether the public salt DEG blocks can support a Table S8 rerun.
- `plot_verified_source_expression.py`: Draws heatmaps from the verified source-study FPKM matrices.

## 06_wrapup

- `summarize_reproduction_scope.py`: Rebuilds the final claim-by-claim reproduction scope table from the recorded result files.

## Running the wrap-up summary

```powershell
D:\conda_envs\blueberry-bzip\python.exe scripts\06_wrapup\summarize_reproduction_scope.py `
  --results-dir results `
  --output-dir results\06_wrapup
```

This reads only files under `results/`, so it can be re-run at any time to confirm that the scope table still matches the data.

