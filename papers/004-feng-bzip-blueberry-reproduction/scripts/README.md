# Scripts

Scripts are grouped by their place in the reproduction workflow.

## 01_supplementary

- `summarize_supplementary.py`: Summarizes Tables S1, S3, and S4 and draws expression heatmaps.
- `summarize_cis_elements.py`: Summarizes promoter cis-element counts from Table S2.

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

