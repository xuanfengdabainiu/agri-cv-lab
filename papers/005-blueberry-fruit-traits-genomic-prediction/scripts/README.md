# Scripts

## Data inspection

Checks required columns, table sizes, Brix coverage, and sample overlap without fitting a model.

```powershell
$env:LC_ALL = "C"
D:\miniconda3\Scripts\conda.exe run -p D:\conda_envs\blueberry-gs Rscript `
  papers\005-blueberry-fruit-traits-genomic-prediction\scripts\inspect_data.R `
  D:\science-data\datasets\blueberry-fruit-traits-genomic-prediction `
  D:\science-data\runs\blueberry-fruit-traits-genomic-prediction\setup\data-inspection.csv
```

## Brix GBLUP baseline

Runs the prepared baseline with 10 repeated 80/20 train-test splits and seed 42.

```powershell
$env:LC_ALL = "C"
D:\miniconda3\Scripts\conda.exe run -p D:\conda_envs\blueberry-gs Rscript `
  papers\005-blueberry-fruit-traits-genomic-prediction\scripts\run_brix_gblup.R `
  D:\science-data\datasets\blueberry-fruit-traits-genomic-prediction `
  D:\science-data\runs\blueberry-fruit-traits-genomic-prediction\brix-gblup-seed42 `
  10 42
```

This baseline was completed on 2026-11-23. See `results/brix-gblup-seed42.md`.

## 2021-to-2022 Brix prediction

Uses Brix measured in 2021 for training and Brix measured in 2022 for evaluation. Samples are explicitly aligned by `germplasmName` before splitting.

```powershell
$env:LC_ALL = "C"
D:\miniconda3\Scripts\conda.exe run -p D:\conda_envs\blueberry-gs Rscript `
  papers\005-blueberry-fruit-traits-genomic-prediction\scripts\run_brix_2021_to_2022.R `
  D:\science-data\datasets\blueberry-fruit-traits-genomic-prediction `
  D:\science-data\runs\blueberry-fruit-traits-genomic-prediction\brix-2021-to-2022-seed42 `
  10 42
```

This experiment was completed on 2026-11-23. See `results/brix-2021-to-2022-seed42.md`.

## Three-year Brix model with year fixed effect

Uses all available 2020–2022 Brix records, hides selected 2022 records, and includes year as a fixed effect. Earlier records from a held-out plant remain available, matching the paper's repeated-record setup.

```powershell
$env:LC_ALL = "C"
D:\miniconda3\Scripts\conda.exe run -p D:\conda_envs\blueberry-gs Rscript `
  papers\005-blueberry-fruit-traits-genomic-prediction\scripts\run_brix_3year_fixed.R `
  D:\science-data\datasets\blueberry-fruit-traits-genomic-prediction `
  D:\science-data\runs\blueberry-fruit-traits-genomic-prediction\brix-3year-fixed-seed42 `
  10 42
```

This experiment was completed on 2026-11-26. See `results/brix-3year-fixed-seed42.md`.

## Audit the author three-year design

```powershell
$env:LC_ALL = "C"
D:\miniconda3\Scripts\conda.exe run -p D:\conda_envs\blueberry-gs Rscript `
  papers\005-blueberry-fruit-traits-genomic-prediction\scripts\audit_author_3year_design.R `
  papers\005-blueberry-fruit-traits-genomic-prediction\results\reference\author-3year-design-perm1.csv `
  papers\005-blueberry-fruit-traits-genomic-prediction\results\tables\author-3year-design-audit.csv
```

This audit was completed on 2026-11-26.

## Three-year averaged Brix

Calculates one mean Brix value per plant from 2020–2022, then runs 10 repeated 80/20 GBLUP splits.

```powershell
$env:LC_ALL = "C"
D:\miniconda3\Scripts\conda.exe run -p D:\conda_envs\blueberry-gs Rscript `
  papers\005-blueberry-fruit-traits-genomic-prediction\scripts\run_brix_3year_average.R `
  D:\science-data\datasets\blueberry-fruit-traits-genomic-prediction `
  D:\science-data\runs\blueberry-fruit-traits-genomic-prediction\brix-3year-average-seed42 `
  10 42
```

This experiment was completed on 2026-11-26. See `results/brix-3year-average-seed42.md`.

## Reusable fruit-trait GBLUP runner

Runs one trait in one of four modes: `within-2022`, `cross-year`, `3year-fixed`, or `3year-average`.

```powershell
$env:LC_ALL = "C"
D:\miniconda3\Scripts\conda.exe run -p D:\conda_envs\blueberry-gs Rscript `
  papers\005-blueberry-fruit-traits-genomic-prediction\scripts\run_trait_gblup.R `
  D:\science-data\datasets\blueberry-fruit-traits-genomic-prediction `
  <output-dir> <long-trait> <2022-trait> <trait-slug> <mode> 10 42
```

Example trait arguments for acidity: `Acidity Acidity_2022 acidity`.

The four acidity modes were completed on 2026-11-27. See `results/acidity-reproduction.md`.

The four pH modes were completed on 2026-11-27 with trait arguments `pH pH_2022 ph`. See `results/ph-reproduction.md`.

The four ratio modes were completed on 2026-11-27 with trait arguments `Ratio Ratio_2022 ratio`. See `results/ratio-reproduction.md`.

The four fruit-mass modes were completed on 2026-11-27 with trait arguments `FruitMass FruitMass_2022 fruit-mass`. See `results/fruit-mass-reproduction.md`.
