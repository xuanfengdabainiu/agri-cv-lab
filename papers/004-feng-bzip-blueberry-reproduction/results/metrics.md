# Metrics

This project is in the setup stage. No reproduction metrics have been produced.

| Run | Date | Analysis | Input | Result | Notes |
|---|---|---|---|---|---|
| setup-001 | 2026-11-13 | project setup | paper and supplementary archive | complete | no raw RNA-seq processing |
| supplementary-001 | 2026-11-13 | supplementary-table summary | S1: VcbZIP basic information; S3: salt RNA-seq; S4: drought RNA-seq | 102 / 18 / 13 | matches the paper's reported bZIP, salt-response, and drought-response counts |
| genome-001 | 2026-11-13 | genome preparation | Draper V1.0 FASTA and GFF | 128,559 proteins / 1,760 scaffolds | passed file-level count checks |
| candidate-001 | 2026-11-13 | bZIP homology candidate screen | 153 paper reference proteins vs. 128,559-protein Draper proteome | 267 candidates | recovered all 153 reference proteins; domain confirmation is pending |
| domain-001 | 2026-11-14 | Pfam bZIP-domain confirmation | 267 homology candidates | 214 domain-confirmed / 153 paper references recovered | 61 additional domain-confirmed candidates require duplicate and completeness filtering |
| cis-element-001 | 2026-11-14 | promoter cis-element summary | Table S2 | 261 ABA-responsive elements across 82 VcbZIP genes | supplementary-table reproduction; genome-derived promoter analysis is pending |
| promoter-001 | 2026-11-14 | genome-derived promoter extraction | Draper V1.0 scaffold FASTA and GFF | 153 sequences for 102 VcbZIP names | one VcbZIP43 copy has only 430 bp upstream due to scaffold boundary |
| phylogeny-001 | 2026-11-14 | preliminary UPGMA phylogeny | 153 VcbZIP protein copies + 78 AtbZIP references | 231 proteins / 2,172 alignment columns | nearest Arabidopsis references mapped; final A-S grouping needs motif evidence |
| structure-001 | 2026-11-14 | exon-intron structure summary | Draper V1.0 GFF | 153 gene copies / exon range 1-14 | gene structure table and exon-count figure generated |
| expression-source-001 | 2026-11-14 | source-study expression verification | 3 original stress-study supplementary workbooks | drought 11/13 exact FPKM; salt 18/18; ABA 6/7 | raw SRA runs are pooled by time point, while supplementary tables preserve three replicates |
| drought-deg-001 | 2026-11-14 | drought DEG list reproduction | source drought DESeq2 comparisons | 11/13 VcbZIP genes recovered | two gene IDs are absent from the source matrix and DEG table |
| salt-deg-001 | 2026-11-14 | salt DEG list reproduction | source salt DESeq2 comparisons | 18/18 VcbZIP genes recovered | all reported salt-responsive genes reproduced at the stated thresholds |
| aba-fpkm-001 | 2026-11-15 | ABA FPKM source verification | source ABA hormone-pathway matrix | 6/7 exact FPKM profiles | VcbZIP1 is absent from the source table |
| expression-heatmap-001 | 2026-11-15 | verified-source heatmaps | drought and ABA source FPKM matrices | drought 11 genes / ABA 6 genes | uses only exact source-matched gene IDs |
| correlation-001 | 2026-11-15 | VcbZIP Pearson correlations | Tables S3/S4 FPKM values | salt max diff 0.027; drought 77/78 pairs close | drought VcbZIP83-VcbZIP45 is the one large mismatch |
| figure8-drought-001 | 2026-11-15 | VcbZIP-stress gene correlation verification | Table S9 and source drought FPKM matrix | 129/140 computable pairs match within 0.001 | 22 pairs cannot be computed because source VcbZIP IDs are missing |

