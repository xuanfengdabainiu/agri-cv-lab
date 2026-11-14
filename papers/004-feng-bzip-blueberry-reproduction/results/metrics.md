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

