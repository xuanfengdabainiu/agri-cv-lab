# Blueberry Brix Genomic Prediction

## Goal

Reproduce the paper's main blueberry sweetness experiment: use SNP genotype data to predict fruit soluble solids (`Brix`).

The first reproduction scope is deliberately small: one Brix prediction pipeline, fixed data split, repeatable metrics, and no full-paper GWAS run.

## Paper

- Title: Genomic prediction enables selection for improved fruit ripening traits in northern highbush blueberry (Vaccinium corymbosum L.) breeding populations
- DOI: https://doi.org/10.1093/g3journal/jkag271
- Code and data: https://github.com/lilyhislop/BlueberryGenomicSelection_USDA-BI
- Local data path (planned): `D:\science-data\datasets\blueberry-brix-genomic-prediction`
- Local run path (planned): `D:\science-data\runs\blueberry-brix-genomic-prediction`

## Status

`reproducing`

The minimal data and R environment are ready. The first 2022 Brix GBLUP baseline has been completed.

## Planned Reproduction

1. Download only the required phenotype table, processed SNP dosage table, and author reproduction script.
2. Verify sample IDs, Brix values, marker counts, and missing values.
3. Adapt hard-coded paths without changing the prediction method.
4. Run a fixed-seed 2022 Brix genomic prediction baseline.
5. Repeat an 80/20 train-test split 10 times and report predictive ability.
6. Run the paper's 2021-to-2022 Brix prediction as a second experiment.
7. Treat GWAS and other traits as optional later work.

## Quick Start

```powershell
$env:LC_ALL = "C"
D:\miniconda3\Scripts\conda.exe run -p D:\conda_envs\blueberry-gs Rscript `
  papers\005-blueberry-brix-genomic-prediction\scripts\run_brix_gblup.R `
  D:\science-data\datasets\blueberry-brix-genomic-prediction `
  D:\science-data\runs\blueberry-brix-genomic-prediction\brix-gblup-seed42 `
  10 42
```

See [`scripts/README.md`](scripts/README.md) for the inspection command and output descriptions.

## Main Results

- Data inspection: [`results/data-inspection.md`](results/data-inspection.md)
- Brix GBLUP baseline: [`results/brix-gblup-seed42.md`](results/brix-gblup-seed42.md)
- 2021-to-2022 prediction: [`results/brix-2021-to-2022-seed42.md`](results/brix-2021-to-2022-seed42.md)
- Experiment metrics: [`results/metrics.md`](results/metrics.md)
- Repeat-level metrics and predictions: [`results/tables/`](results/tables/)
- Mean predictive ability: **0.4024**, close to the paper's approximately **0.41** result for its 2022 training set.
- ID-matched 2021-to-2022 predictive ability: **0.3327**, close to the paper's approximately **0.35** result.

## Repository Rules

- Keep downloaded data under `D:\science-data\datasets`.
- Keep generated runs under `D:\science-data\runs`.
- Commit small CSV result tables so experiments can be reviewed from GitHub.
- Do not commit the full upstream repository or large generated files.
- Update `reproduction-log.md` and `results/metrics.md` for every run.
