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
