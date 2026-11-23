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
