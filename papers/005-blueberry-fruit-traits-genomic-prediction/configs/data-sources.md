# Data Sources

## Upstream Repository

- URL: https://github.com/lilyhislop/BlueberryGenomicSelection_USDA-BI
- Full repository size observed during feasibility review: approximately 5.3 GB
- Full repository download: deferred and unnecessary for the first reproduction stage

## Minimal Files Planned

| Purpose | Upstream path | Approximate size |
|---|---|---:|
| Reproduction code | `BIProject/Code/BIProject_rrBLUP_GS_Script_G3SubmissionReproducability.R` | 0.05 MB |
| 2022 phenotypes | `BIProject/Data/OutputtedData/BIProject_2022Pheno_WithParentsandNoOutliers.csv` | 1.26 MB |
| Multi-year phenotypes | `BIProject/Data/OutputtedData/BIProject_LongPhenoType_ByYear.csv` | 1.22 MB |
| Processed SNP dosage | `BIProject/Data/OutputtedData/GenoInfo/BIProject_compiled_variants_v2_Dosage_minDepth64_maxMiss.05_minMinor250.csv` | 15.99 MB |

## Download Status and SHA-256

The four minimal files were downloaded on 2026-11-23. They are stored outside Git.

| Local file | Bytes | SHA-256 |
|---|---:|---|
| `source/author-reproduction.R` | 53,666 | `37BC8786FE01A7FE02DCB8EAF01541C814CDF06E18530F348FA5A039FAD7D02E` |
| `phenotype/BIProject_2022Pheno_WithParentsandNoOutliers.csv` | 1,318,636 | `E4E9514930D1451F8E5743E3913B17CB8F76B482400E1DC2881308D683057C72` |
| `phenotype/BIProject_LongPhenoType_ByYear.csv` | 1,279,341 | `F514AACC2A7C00AF88414A84765FF8B9A3CFA6D0FCFA34612B9A105A8A4995E8` |
| `genotype/BIProject_compiled_variants_v2_Dosage_minDepth64_maxMiss.05_minMinor250.csv` | 16,769,470 | `5A02CC443AB45D3AD96F49EE70689F017BA9A8C604D23FFB4AC435246F80AF0A` |

## Local Storage Plan

```text
D:\science-data\datasets\blueberry-fruit-traits-genomic-prediction\
|- source\
|- phenotype\
`- genotype\
```

Downloaded data must remain outside Git.

## Author Three-Year Diagnostic Outputs

Two small public author outputs were added on 2026-11-26 to audit the three-year split. Review copies are committed under `results/reference`.

| File | SHA-256 |
|---|---|
| `author-3year-10perm-20pct-metrics.csv` | `5B0B0D97E77F46DFC9CD8A4ECB73306D0B6E35D7006CDDC3F69E091190A927BC` |
| `author-3year-design-perm1.csv` | `104BF950BE9A0427BB70CE3C9ECB8FB6BFB3B04CC3FD027B7366F544CC5A2C7E` |
| `author-3year-average-1000perm-metrics.csv` | `1DA34C26EA46F7E02C2F70E81C4C378CA6F0799E7D2288B78FF2B6C8A835B070` |
