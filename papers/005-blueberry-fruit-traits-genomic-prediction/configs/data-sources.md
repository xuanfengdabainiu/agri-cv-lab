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

## Author Acidity Reference Outputs

| File | SHA-256 |
|---|---|
| `author-acidity-within-2022-1000perm-metrics.csv` | `C927C819107348B1925804BEE6BF578172DDEB9B0D66302009720DD9D32C557C` |
| `author-acidity-cross-year-1000perm-metrics.csv` | `38DFA54186C785E33867AAF0E404AC8FD509441B45E63AECB5E7A74F5F10909B` |
| `author-acidity-3year-fixed-1000perm-metrics.csv` | `31930BC3DF5F471E0F71ED75F09067E55B4651921CE45C869C70520503B94981` |
| `author-acidity-3year-average-1000perm-metrics.csv` | `AAD790EDCF2DA6DE89402711301E0FCF9509B5B4B22BC13F6EAD844C430878CB` |
| `author-acidity-3year-design-perm1.csv` | `995AD9900A50C9F598FB713840F9B2D7CADDFBEC1110DA0DC7C173CF3C081898` |

## Author pH Reference Outputs

| File | SHA-256 |
|---|---|
| `author-ph-within-2022-1000perm-metrics.csv` | `EFF983532D5B992EBD47363D0834CB2FF14FD884F77012408B378708EF0B3078` |
| `author-ph-cross-year-1000perm-metrics.csv` | `7C9C4FA671905B356613F51284E4FE20E9035A56971F8A81F3BF7F953318BC8C` |
| `author-ph-3year-fixed-1000perm-metrics.csv` | `DCE0B6E0A1A138EB881BC276FB5F1FB4A8FB5DE5B061D4F59F86C0CD1E591924` |
| `author-ph-3year-average-1000perm-metrics.csv` | `D5FB0E86FE6524D04605E4689A360A6F410E1C8D41BD07EE4CD156D5590BF747` |
| `author-ph-3year-design-perm1.csv` | `E51CD5F35DD251E41F35D9398CBCE103754EE05A1B173F8A703BAF116FCE31B6` |

## Author Ratio Reference Outputs

The author repository does not contain 1000-repeat within-2022 or cross-year Ratio outputs.

| File | SHA-256 |
|---|---|
| `author-ratio-3year-fixed-1000perm-metrics.csv` | `74D02C93ADAE73412011D47DA9DEF5E6ABCB58B4F62D349D6CB1D751CB93B36C` |
| `author-ratio-3year-average-1000perm-metrics.csv` | `F0324E84DDB2F74B8451EFB9791840DF06AA0BBED1417068673013575E7214A4` |
| `author-ratio-3year-design-perm1.csv` | `CB5A91504FE6F31325EBE3DAD50AEFF68D042C9960E3504C4686858E75726F8E` |

## Author Fruit-Mass Reference Outputs

The author repository does not contain a 1000-repeat cross-year fruit-mass output.

| File | SHA-256 |
|---|---|
| `author-fruit-mass-within-2022-1000perm-metrics.csv` | `F7CF077C0EA7859B56BF9A89BA79E5687BD6FB892EAB6B01C34747D4A7F8AED2` |
| `author-fruit-mass-3year-fixed-1000perm-metrics.csv` | `540D34CE2123843A9E3193EF66D4F29A35FD25DFFC57DA548E1AB59137874912` |
| `author-fruit-mass-3year-average-1000perm-metrics.csv` | `1F8BAE5377A4A40812EEB75D02E0237A5F9FE725EA1FF972FDAA06FBFFD4CA3D` |
| `author-fruit-mass-3year-design-perm1.csv` | `6E7A5DD6102F076D06FA686800D546406028B83DF6AA85B641DD5EB1F679B5CD` |

## Author Height Reference Outputs

| File | SHA-256 |
|---|---|
| `author-height-within-2022-1000perm-metrics.csv` | `8E1A3B4863F7E3B4A5E5C5021679C2CA28B0B637884004E6D624FDDF0F4FF56B` |
| `author-height-cross-year-1000perm-metrics.csv` | `3C36AF9BEE953E503C78C8620B38A15360B6E2147DAE9145632E62DE90B52E3B` |
| `author-height-3year-fixed-10perm-metrics.csv` | `B6AAB66676A7FD40662543FB425F429D1FE6DEEB04168657D1B6C376A5924C58` |
| `author-height-3year-average-1000perm-metrics.csv` | `6662B7D3A1921CFF9E806B548BB754818B90A54C1ADA282EE75D80266CE319C4` |
| `author-height-3year-design-perm1.csv` | `37C18C0D396CEFCAF31B8C7D1E11BE440E5E54D4C7A14CA763160179708D9116` |

## Author Bloom-50% Reference Outputs

| File | SHA-256 |
|---|---|
| `author-bloom50-within-2022-1000perm-metrics.csv` | `0EC09030AD4E89968A20FAE48523B0D3355EF9FB1E34946F84B11AD32B1E0491` |
| `author-bloom50-cross-year-1000perm-metrics.csv` | `4074D28C1336A1F062DB7C449F74433893CDD7727011E3DE9648064BED3059FD` |
| `author-bloom50-fixed-1000perm-metrics.csv` | `4AEE17192CE0CFA81E4C5121B0B10A59CEDB2C570A3C67EC8FCFC41F509F16BF` |
| `author-bloom50-average-1000perm-metrics.csv` | `26BF4DD264BF4AD4FB90B0F466AD1087B300797048A52FD5A6AFD1107351F05E` |
| `author-bloom50-3year-design-perm1.csv` | `949F2BEEA69C44FF4ED9D0DB735147FDC75B707771C2FF1238ACF96596198A48` |
