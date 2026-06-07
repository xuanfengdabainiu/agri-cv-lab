# Agri CV Lab

This repository is my unified lab notebook for agricultural computer vision reproduction and experiments.

## Repository Layout

```text
agri-cv-lab/
├─ papers/                 # One folder per paper or experiment
├─ shared/
│  ├─ templates/           # Reusable experiment templates
│  └─ utils/               # Shared scripts used across experiments
├─ envs/                   # Conda / pip environment files
└─ docs/                   # Cross-project notes and indexes
```

## What Goes Into Git

Commit:

- code and scripts
- configs
- paper notes
- reproduction logs
- small result figures
- metric summaries

Do not commit:

- datasets
- full training runs
- model weights
- API keys
- large archives

## Local Data Storage

Large files are stored outside this repository:

```text
D:\science-data\
├─ datasets\
├─ runs\
└─ weights\
```

Use this repository for code, configs, notes, and concise result summaries.

## Standard Experiment Folder

Each experiment under `papers/` should follow this structure:

```text
papers/000-experiment-slug/
├─ README.md
├─ paper-notes.md
├─ reproduction-log.md
├─ configs/
├─ scripts/
└─ results/
   ├─ metrics.md
   └─ figures/
```

Use `shared/templates/experiment/` when creating a new experiment.
