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
- Planned external data path: `D:\science-data\datasets\blueberry-fruit-traits-genomic-prediction`.
- Planned run path: `D:\science-data\runs\blueberry-fruit-traits-genomic-prediction`.
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
  papers\005-blueberry-fruit-traits-genomic-prediction\scripts\inspect_data.R `
  D:\science-data\datasets\blueberry-fruit-traits-genomic-prediction `
  D:\science-data\runs\blueberry-fruit-traits-genomic-prediction\setup\data-inspection.csv
```

Config Changes:

- Added `configs/environment.yml`.
- Downloaded the four minimal upstream files listed in `configs/data-sources.md`.
- Added a read-only data inspection script.
- Added a prepared Brix-only GBLUP script with 10 repeated 80/20 splits and seed 42.
- Kept the fixed object-detection metrics header required by this repository; non-applicable fields remain `N/A`.
- Zotero/PDF work was paused at the user's request; no Zotero item or PDF was added.

Run Output:

- Machine-readable inspection: `D:\science-data\runs\blueberry-fruit-traits-genomic-prediction\setup\data-inspection.csv`
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
  papers\005-blueberry-fruit-traits-genomic-prediction\scripts\run_brix_gblup.R `
  D:\science-data\datasets\blueberry-fruit-traits-genomic-prediction `
  D:\science-data\runs\blueberry-fruit-traits-genomic-prediction\brix-gblup-seed42 `
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

- Metrics: `D:\science-data\runs\blueberry-fruit-traits-genomic-prediction\brix-gblup-seed42\brix-gblup-metrics.csv`
- Predictions: `D:\science-data\runs\blueberry-fruit-traits-genomic-prediction\brix-gblup-seed42\brix-gblup-predictions.csv`
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
  papers\005-blueberry-fruit-traits-genomic-prediction\scripts\run_brix_2021_to_2022.R `
  D:\science-data\datasets\blueberry-fruit-traits-genomic-prediction `
  D:\science-data\runs\blueberry-fruit-traits-genomic-prediction\brix-2021-to-2022-seed42 `
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

- Metrics: `D:\science-data\runs\blueberry-fruit-traits-genomic-prediction\brix-2021-to-2022-seed42\brix-2021-to-2022-metrics.csv`
- Predictions: `D:\science-data\runs\blueberry-fruit-traits-genomic-prediction\brix-2021-to-2022-seed42\brix-2021-to-2022-predictions.csv`
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
  papers\005-blueberry-fruit-traits-genomic-prediction\scripts\run_brix_3year_fixed.R `
  D:\science-data\datasets\blueberry-fruit-traits-genomic-prediction `
  D:\science-data\runs\blueberry-fruit-traits-genomic-prediction\brix-3year-fixed-seed42 `
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

## 2026-11-26: three-year averaged Brix and Brix-scope close-out

Goal:

- Reproduce the paper's three-year averaged Brix setup.
- Compare against the author's public 1000-repeat output.
- Close the selected Brix genomic-prediction scope.

Environment:

- Environment: `D:\conda_envs\blueberry-gs`
- R: 4.4.3
- rrBLUP: 4.6.3
- GPU: not required

Command:

```powershell
$env:LC_ALL = "C"
D:\miniconda3\Scripts\conda.exe run -p D:\conda_envs\blueberry-gs Rscript `
  papers\005-blueberry-fruit-traits-genomic-prediction\scripts\run_brix_3year_average.R `
  D:\science-data\datasets\blueberry-fruit-traits-genomic-prediction `
  D:\science-data\runs\blueberry-fruit-traits-genomic-prediction\brix-3year-average-seed42 `
  10 42
```

Configuration:

- Source phenotype records: 4,849
- One averaged Brix value per plant: 2,960
- Markers: 1,822
- Split: 80% train / 20% test
- Repeats: 10
- Seed: 42
- Per repeat: 2,368 training plants and 592 test plants
- Imputation: mean, matching the effective fallback used by `A.mat` in previous runs

Run Output:

- Metrics: `results/tables/brix-3year-average-metrics.csv`
- Predictions: `results/tables/brix-3year-average-predictions.csv`
- Assignments: `results/tables/brix-3year-average-assignments.csv`
- Stable summary: `results/brix-3year-average-seed42.md`
- Author reference: `results/reference/author-3year-average-1000perm-metrics.csv`

Results:

- Mean Pearson predictive ability: 0.4558
- Pearson standard deviation: 0.0320
- Pearson range: 0.3904 to 0.4935
- Mean Spearman correlation: 0.4401
- Mean MSE: 3.0580
- Mean heritability: 0.5073
- Completed repeats: 10/10
- Prediction rows: 5,920
- Assignment rows: 29,600
- Missing predictive-ability values: 0
- Author public 1000-repeat Pearson mean: 0.4555
- Paper rounded references: predictive ability 0.46; heritability 0.51

Problems:

- The earlier three-year fixed-effect run spent several minutes attempting EM imputation before falling back to mean imputation.

Fixes:

- Used mean imputation directly because it is the effective method selected by `A.mat` for this linearly dependent marker matrix.
- The complete averaged-phenotype run finished in approximately 38 seconds.

Conclusion:

- The three-year averaged Brix result closely reproduces both predictive ability and heritability.
- Three of four selected Brix configurations reproduce the paper closely.
- The remaining three-year fixed-effect mismatch is explained and documented by the public split audit.
- The Brix genomic-prediction reproduction scope is complete.

Next Step:

- Begin an improvement phase only after reviewing the final summary with the advisor.
- Candidate improvement: compare GBLUP with ridge regression, Random Forest, and XGBoost on identical saved splits.

## 2026-11-26: project rename and scope expansion

Goal:

- Rename paper 005 so the directory represents the paper's broader fruit-quality and ripening-trait scope.
- Keep the completed Brix work as the first finished trait phase.

Changes:

- Renamed `papers/005-blueberry-brix-genomic-prediction` to `papers/005-blueberry-fruit-traits-genomic-prediction`.
- Renamed the external dataset directory to `D:\science-data\datasets\blueberry-fruit-traits-genomic-prediction`.
- Renamed the external run directory to `D:\science-data\runs\blueberry-fruit-traits-genomic-prediction`.
- Updated all repository commands and local-path references to the new name.
- Changed the README title to `Blueberry Fruit-Trait Genomic Prediction`.
- Changed the project status from `done` to `reproducing`; the Brix phase remains explicitly `done`.
- Expanded the next scope to acidity, pH, and Brix-to-acidity ratio.
- Kept Brix-specific result filenames unchanged because they accurately describe completed runs.
- Kept the `blueberry-gs` conda environment name because it is already trait-neutral.

Command:

```text
No model was run. This step only moved directories and updated project documentation and runnable paths.
```

Conclusion:

- The repository name now matches the paper-level scope.
- Existing Brix commands remain runnable from the new repository and D-drive paths.
- The Brix phase is complete; the broader paper reproduction continues.

Next Step:

- Reproduce titratable acidity with the same four training setups used for Brix.
- Then reproduce pH and Brix-to-acidity ratio.

## 2026-11-27: titratable-acidity four-mode reproduction

Goal:

- Reproduce acidity prediction in the same four modes used for Brix.
- Generalize the implementation so pH and Brix-to-acidity ratio can reuse one script.

Environment:

- Environment: `D:\conda_envs\blueberry-gs`
- R: 4.4.3
- rrBLUP: 4.6.3
- GPU: not required

Implementation:

- Added `scripts/run_trait_gblup.R`.
- Modes: `within-2022`, `cross-year`, `3year-fixed`, and `3year-average`.
- Trait arguments: `Acidity Acidity_2022 acidity`.
- All modes use 1,822 SNPs, 10 repeats, seed 42, 80/20 splits, mean imputation, and saved assignments.
- Cross-year samples are matched by `germplasmName`.
- The fixed-effect mode hides every selected plant's 2022 acidity before fitting.

Commands:

```powershell
$env:LC_ALL = "C"
$modes = @("within-2022", "cross-year", "3year-fixed", "3year-average")
foreach ($mode in $modes) {
  D:\miniconda3\Scripts\conda.exe run -p D:\conda_envs\blueberry-gs Rscript `
    papers\005-blueberry-fruit-traits-genomic-prediction\scripts\run_trait_gblup.R `
    D:\science-data\datasets\blueberry-fruit-traits-genomic-prediction `
    D:\science-data\runs\blueberry-fruit-traits-genomic-prediction\acidity-$mode-seed42 `
    Acidity Acidity_2022 acidity $mode 10 42
}
```

Results:

- 2022 -> 2022: Pearson 0.4613 +/- 0.0269; author 0.4710
- 2021 -> 2022: Pearson 0.3749 +/- 0.0362; author 0.3554
- Three-year fixed effect: Pearson 0.5044 +/- 0.0338; author 0.6449
- Three-year average: Pearson 0.5462 +/- 0.0229; author 0.5624
- All 40 runs completed without missing predictive-ability values.
- Stable summary: `results/acidity-reproduction.md`

Author Split Audit:

- Author design rows: 4,766
- Rows labelled test: 587 across 528 plant IDs
- Test rows by year: 193 from 2020, 176 from 2021, 218 from 2022
- Test IDs retaining another training record: 382
- Test IDs retaining their 2022 acidity target in training: 201
- Audit output: `results/tables/author-acidity-3year-design-audit.csv`

Conclusion:

- The within-year, cross-year, and three-year-average acidity setups closely reproduce the author outputs.
- The ID-safe fixed-effect setup does not reproduce the inflated author value.
- The acidity phase independently confirms the split problem found during Brix reproduction.
- The reusable runner is ready for pH and Brix-to-acidity ratio.

Next Step:

- Reproduce pH in the four modes.
- Then reproduce Brix-to-acidity ratio.
