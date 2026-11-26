# Reproduction Log

## 2026-11-23: project setup and feasibility review

Goal:

- Create the paper 005 experiment structure.
- Define a small and realistic reproduction scope for the paper's Brix genomic prediction experiment.

Environment:

- OS: Windows
- Available RAM: approximately 15.2 GB
- Available D-drive space at review time: approximately 139.5 GB
- R environment: not created
- Required R packages: planned (`rrBLUP`, `GWASpoly`, `tidyverse`, `ggpubr`)

Commands:

```text
No model or analysis command was run.
```

Config Changes:

- Created the standard experiment files.
- Planned external data path: `D:\science-data\datasets\blueberry-brix-genomic-prediction`.
- Planned run path: `D:\science-data\runs\blueberry-brix-genomic-prediction`.
- Limited the first reproduction to Brix prediction; full GWAS and other traits are outside the first stage.

Results:

- Feasibility: suitable for a reduced reproduction on this computer.
- Upstream repository: about 5.3 GB and 18,075 files.
- Essential processed inputs identified during review:
  - 2022 phenotype table: about 1.26 MB
  - multi-year phenotype table: about 1.22 MB
  - processed SNP dosage table: about 15.99 MB
  - author reproduction script: about 0.05 MB
- No data or upstream code was downloaded into this project.

Problems:

- The author script has a hard-coded Windows path.
- The author script mixes Brix prediction, other traits, and GWAS in one file.
- The random seed is commented out.
- R is not currently available from the command line.

Fixes:

- Plan a Brix-only wrapper with project-relative paths and a fixed seed.
- Download only the essential files before the first run.

Conclusion:

- A method-level Brix reproduction is feasible.
- An exact, unchanged full-paper rerun is not the first target.

Next Step:

- Obtain the paper PDF through Zotero.
- Download only the four essential upstream files.
- Create and verify the minimal R environment before running a data inspection smoke test.

## 2026-11-23: minimal data and environment preparation

Goal:

- Prepare all inputs and code needed before the first Brix prediction run.
- Avoid downloading the full 5.3 GB upstream repository.

Environment:

- OS: Windows
- Conda: `D:\miniconda3`
- Environment: `D:\conda_envs\blueberry-gs`
- R: 4.4.3
- rrBLUP: 4.6.3
- CUDA/GPU: not required

Commands:

```powershell
D:\miniconda3\Scripts\conda.exe create -y -p D:\conda_envs\blueberry-gs `
  -c conda-forge r-base=4.4 r-rrblup

$env:LC_ALL = "C"
D:\miniconda3\Scripts\conda.exe run -p D:\conda_envs\blueberry-gs Rscript `
  papers\005-blueberry-brix-genomic-prediction\scripts\inspect_data.R `
  D:\science-data\datasets\blueberry-brix-genomic-prediction `
  D:\science-data\runs\blueberry-brix-genomic-prediction\setup\data-inspection.csv
```

Config Changes:

- Added `configs/environment.yml`.
- Downloaded the four minimal upstream files listed in `configs/data-sources.md`.
- Added a read-only data inspection script.
- Added a prepared Brix-only GBLUP script with 10 repeated 80/20 splits and seed 42.
- Kept the fixed object-detection metrics header required by this repository; non-applicable fields remain `N/A`.
- Zotero/PDF work was paused at the user's request; no Zotero item or PDF was added.

Run Output:

- Machine-readable inspection: `D:\science-data\runs\blueberry-brix-genomic-prediction\setup\data-inspection.csv`
- Stable summary: `results/data-inspection.md`

Results:

- 2022 phenotype rows: 4,368
- Multi-year phenotype rows: 9,806
- Non-missing 2022 Brix values: 2,110
- SNP markers: 1,822
- Genotyped samples: 4,494
- Samples with both Brix and SNP data: 1,935
- Brix range: 8.5 to 21.7; mean 15.2075
- `run_brix_gblup.R` passed an R syntax check.

Problems:

- Direct `conda-forge` access timed out during the first environment attempt.
- R emitted locale warnings when `C.UTF-8` was inherited on Windows.

Fixes:

- Used the configured Tsinghua conda-forge mirror to complete installation.
- Set `LC_ALL=C` in the documented run commands.

Conclusion:

- Minimal data, environment, validation, and baseline code are ready.
- No formal prediction experiment has been run, so no predictive metric is reported yet.

Next Step:

- Run `run_brix_gblup.R` for the first 10-repeat seed-42 baseline.
- Record predictive ability in this log and `results/metrics.md`.

## 2026-11-23: 2022 Brix GBLUP baseline

Goal:

- Run the first formal Brix genomic prediction baseline.
- Compare the reproduced predictive ability with the paper's 2022-training result.

Environment:

- Environment: `D:\conda_envs\blueberry-gs`
- R: 4.4.3
- rrBLUP: 4.6.3
- GPU: not required

Command:

```powershell
$env:LC_ALL = "C"
D:\miniconda3\Scripts\conda.exe run -p D:\conda_envs\blueberry-gs Rscript `
  papers\005-blueberry-brix-genomic-prediction\scripts\run_brix_gblup.R `
  D:\science-data\datasets\blueberry-brix-genomic-prediction `
  D:\science-data\runs\blueberry-brix-genomic-prediction\brix-gblup-seed42 `
  10 42
```

Configuration:

- Trait: `Brix_2022`
- Model: GBLUP using `rrBLUP::kin.blup`
- Samples: 1,935
- Markers: 1,822
- Split: 80% train / 20% test
- Repeats: 10
- Seed: 42
- Per repeat: 1,548 training samples and 387 test samples

Run Output:

- Metrics: `D:\science-data\runs\blueberry-brix-genomic-prediction\brix-gblup-seed42\brix-gblup-metrics.csv`
- Predictions: `D:\science-data\runs\blueberry-brix-genomic-prediction\brix-gblup-seed42\brix-gblup-predictions.csv`
- Stable summary: `results/brix-gblup-seed42.md`

Results:

- Mean predictive ability: 0.4024
- Standard deviation: 0.0327
- Minimum: 0.3671
- Maximum: 0.4590
- Completed repeats: 10/10
- Prediction rows: 3,870
- Missing predictive-ability values: 0
- Paper comparison: close to the approximately 0.41 predictive ability reported for the 2022 training set.

Problems:

- `rrBLUP::A.mat` reported linear dependence among genotype rows.

Fixes:

- `rrBLUP` automatically fell back from EM imputation to mean imputation and completed normally.
- The fallback is preserved and reported rather than hidden.

Conclusion:

- The first Brix GBLUP baseline reproduces the paper's 2022-training predictive ability closely.
- This confirms that the downloaded processed data and the reduced pipeline are usable.

Next Step:

- Reproduce the paper's 2021-to-2022 Brix prediction.
- Then test the combined three-year training setup, which the paper reports as stronger.

## 2026-11-23: ID-matched 2021-to-2022 Brix prediction

Goal:

- Train from 2021 Brix and evaluate predictions against 2022 Brix.
- Prevent cross-year sample mismatches by aligning the two years by plant ID.

Environment:

- Environment: `D:\conda_envs\blueberry-gs`
- R: 4.4.3
- rrBLUP: 4.6.3
- GPU: not required

Command:

```powershell
$env:LC_ALL = "C"
D:\miniconda3\Scripts\conda.exe run -p D:\conda_envs\blueberry-gs Rscript `
  papers\005-blueberry-brix-genomic-prediction\scripts\run_brix_2021_to_2022.R `
  D:\science-data\datasets\blueberry-brix-genomic-prediction `
  D:\science-data\runs\blueberry-brix-genomic-prediction\brix-2021-to-2022-seed42 `
  10 42
```

Configuration:

- Model: GBLUP using `rrBLUP::kin.blup`
- Training phenotype: 2021 Brix
- Evaluation phenotype: 2022 Brix
- ID-matched samples: 1,019
- Markers: 1,822
- Split: 80% train / 20% held out
- Repeats: 10
- Seed: 42
- Per repeat: 815 training samples and 204 test samples

Run Output:

- Metrics: `D:\science-data\runs\blueberry-brix-genomic-prediction\brix-2021-to-2022-seed42\brix-2021-to-2022-metrics.csv`
- Predictions: `D:\science-data\runs\blueberry-brix-genomic-prediction\brix-2021-to-2022-seed42\brix-2021-to-2022-predictions.csv`
- Stable summary: `results/brix-2021-to-2022-seed42.md`

Results:

- Mean Pearson predictive ability: 0.3327
- Pearson standard deviation: 0.0677
- Pearson range: 0.2486 to 0.4383
- Mean Spearman correlation: 0.2876
- Mean MSE: 4.2978
- Completed repeats: 10/10
- Prediction rows: 2,040
- Missing predictive-ability values: 0
- Paper comparison: close to the approximately 0.35 predictive ability reported for its 2021 training set.

Problems:

- The upstream script creates 2021 and 2022 tables separately but later compares them by row position.
- Only 1,019 plants have Brix in both years and matching SNP data, so row-position comparison risks mismatching plants.
- `rrBLUP::A.mat` again detected linear dependence among genotype rows.

Fixes:

- Matched both yearly phenotype tables to genotype columns by `germplasmName` before splitting.
- Added an assertion that the aligned 2021 and 2022 ID order is identical.
- Preserved and recorded `rrBLUP`'s automatic mean-imputation fallback.

Conclusion:

- The corrected, ID-matched result remains close to the paper's reported value.
- Cross-year predictive ability is lower than the reproduced 2022 within-year result, showing the added difficulty of year-to-year variation.

Next Step:

- Reproduce the combined three-year Brix training setup with year as a fixed effect.
- Compare within-year, cross-year, and combined-year predictive ability in one table.

## 2026-11-23: result storage and metrics format correction

Goal:

- Make the experiment results directly reviewable from GitHub.
- Replace the object-detection metrics columns with genomic-prediction metrics.

Command:

```text
No model was run. Existing CSV outputs were copied from the D-drive run folders into results/tables.
```

Changes:

- Replaced the detection-oriented `metrics.md` columns with model, year direction, samples, SNPs, repeats, seed, Pearson, Spearman, MSE, and paper reference.
- Removed setup-only rows from `metrics.md`; setup history remains in this reproduction log.
- Added all four repeat-level metric and prediction CSV files under `results/tables`.
- Renamed the result-note section from `External Outputs` to `Output Files` and linked the committed CSV files.
- Clarified in `docs/workflow.md` that small result tables can be committed.

File Sizes:

- 2022 within-year metrics: 379 bytes
- 2022 within-year predictions: 165,576 bytes
- 2021-to-2022 metrics: 1,276 bytes
- 2021-to-2022 predictions: 97,097 bytes
- Total: 264,328 bytes, approximately 258 KB

Conclusion:

- These files are small and belong in GitHub.
- D-drive run folders remain the original machine outputs; GitHub now contains reviewable copies.
- `results/metrics.md` now matches the actual task instead of displaying unused mAP fields.

Next Step:

- Use the same analysis-oriented metrics columns for the combined three-year experiment.

## 2026-11-26: three-year Brix model and author split audit

Goal:

- Reproduce the combined 2020–2022 Brix model with year as a fixed effect.
- Evaluate against held-out 2022 records while preventing direct 2022-target leakage.
- Investigate any difference from the paper's approximately 0.59 predictive ability.

Environment:

- Environment: `D:\conda_envs\blueberry-gs`
- R: 4.4.3
- rrBLUP: 4.6.3
- GPU: not required
- Peak observed R working memory: approximately 2.9 GB

Command:

```powershell
$env:LC_ALL = "C"
D:\miniconda3\Scripts\conda.exe run -p D:\conda_envs\blueberry-gs Rscript `
  papers\005-blueberry-brix-genomic-prediction\scripts\run_brix_3year_fixed.R `
  D:\science-data\datasets\blueberry-brix-genomic-prediction `
  D:\science-data\runs\blueberry-brix-genomic-prediction\brix-3year-fixed-seed42 `
  10 42
```

Configuration:

- Phenotype records: 4,849
- Model genotypes: 2,960
- 2022 evaluation plants: 1,935
- Markers: 1,822
- Fixed effect: year
- Split: 20% of 2022 plant IDs held out per repeat
- Repeats: 10
- Seed: 42
- Training records per repeat: 4,462
- Test plants per repeat: 387
- Earlier 2020/2021 records remain available for a held-out plant, matching the repeated-record setup.
- Every selected plant's 2022 Brix is removed from training before fitting.

Run Output:

- Metrics: `results/tables/brix-3year-fixed-metrics.csv`
- Predictions: `results/tables/brix-3year-fixed-predictions.csv`
- Assignments: `results/tables/brix-3year-fixed-assignments.csv`
- Stable summary: `results/brix-3year-fixed-seed42.md`

Results:

- Mean Pearson predictive ability: 0.4201
- Pearson standard deviation: 0.0457
- Pearson range: 0.3740 to 0.5353
- Mean Spearman correlation: 0.4118
- Mean MSE: 4.1328
- Mean heritability: 0.4927
- Completed repeats: 10/10
- Missing predictive-ability values: 0
- Paper reference: predictive ability approximately 0.59; heritability approximately 0.49
- Heritability reproduced closely; predictive ability did not reproduce under the ID-safe split.

Problems:

- `A.mat` again detected linear dependence and automatically changed EM imputation to mean imputation.
- The three-year run was substantially slower than the single-year runs because the kinship matrix expanded to 2,960 genotypes.
- The author's public 10-repeat output averages 0.579 Pearson, while the ID-safe reproduction averages 0.4201.

Author Split Audit:

- Downloaded the public 10-repeat metrics and `Perm1` design matrix from the author repository.
- Added `scripts/audit_author_3year_design.R` and generated `results/tables/author-3year-design-audit.csv`.
- Author design rows: 4,849
- Rows labelled test: 592 across 535 plant IDs
- Test rows by year: 178 from 2020, 170 from 2021, 244 from 2022
- Test plant IDs retaining another training record: 405
- Test plant IDs retaining their 2022 Brix target in training: 196
- The upstream correlation code also uses numeric row indexes across genotype-level predictions and record-level 2022 observations.

Conclusion:

- Computer configuration is sufficient; the run used about 2.9 GB R memory and no GPU.
- The data and model reproduce the paper's heritability.
- The paper's three-year predictive ability is not supported after ensuring every held-out 2022 target is absent from training.
- The difference is documented as a split-implementation issue rather than adjusted away.

Next Step:

- Reproduce the paper's three-year averaged-phenotype setup.
- Then close the Brix reproduction with a final comparison and limitations section.
