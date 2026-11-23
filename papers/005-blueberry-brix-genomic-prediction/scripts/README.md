# Scripts

## Data inspection

Checks required columns, table sizes, Brix coverage, and sample overlap without fitting a model.

```powershell
$env:LC_ALL = "C"
D:\miniconda3\Scripts\conda.exe run -p D:\conda_envs\blueberry-gs Rscript `
  papers\005-blueberry-brix-genomic-prediction\scripts\inspect_data.R `
  D:\science-data\datasets\blueberry-brix-genomic-prediction `
  D:\science-data\runs\blueberry-brix-genomic-prediction\setup\data-inspection.csv
```

## Brix GBLUP baseline

Runs the prepared baseline with 10 repeated 80/20 train-test splits and seed 42.

```powershell
$env:LC_ALL = "C"
D:\miniconda3\Scripts\conda.exe run -p D:\conda_envs\blueberry-gs Rscript `
  papers\005-blueberry-brix-genomic-prediction\scripts\run_brix_gblup.R `
  D:\science-data\datasets\blueberry-brix-genomic-prediction `
  D:\science-data\runs\blueberry-brix-genomic-prediction\brix-gblup-seed42 `
  10 42
```

This baseline was completed on 2026-11-23. See `results/brix-gblup-seed42.md`.

## 2021-to-2022 Brix prediction

Uses Brix measured in 2021 for training and Brix measured in 2022 for evaluation. Samples are explicitly aligned by `germplasmName` before splitting.

```powershell
$env:LC_ALL = "C"
D:\miniconda3\Scripts\conda.exe run -p D:\conda_envs\blueberry-gs Rscript `
  papers\005-blueberry-brix-genomic-prediction\scripts\run_brix_2021_to_2022.R `
  D:\science-data\datasets\blueberry-brix-genomic-prediction `
  D:\science-data\runs\blueberry-brix-genomic-prediction\brix-2021-to-2022-seed42 `
  10 42
```

This experiment was completed on 2026-11-23. See `results/brix-2021-to-2022-seed42.md`.
