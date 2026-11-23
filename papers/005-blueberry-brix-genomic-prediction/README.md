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

`planned`

The experiment structure and reproduction scope are ready. No paper data, author repository, or R environment has been downloaded for this project.

## Planned Reproduction

1. Download only the required phenotype table, processed SNP dosage table, and author reproduction script.
2. Verify sample IDs, Brix values, marker counts, and missing values.
3. Adapt hard-coded paths without changing the prediction method.
4. Run a fixed-seed 2022 Brix genomic prediction baseline.
5. Repeat an 80/20 train-test split 10 times and report predictive ability.
6. Run the paper's 2021-to-2022 Brix prediction as a second experiment.
7. Treat GWAS and other traits as optional later work.

## Planned Commands

Commands will be added after the minimal R environment and required input files are confirmed.

## Main Results

See [`results/metrics.md`](results/metrics.md). No experiment has been run yet.

## Repository Rules

- Keep downloaded data under `D:\science-data\datasets`.
- Keep generated runs under `D:\science-data\runs`.
- Do not commit the full upstream repository or large generated files.
- Update `reproduction-log.md` and `results/metrics.md` for every run.
