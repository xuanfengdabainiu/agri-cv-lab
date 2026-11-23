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

The baseline command is prepared but has not been run.
