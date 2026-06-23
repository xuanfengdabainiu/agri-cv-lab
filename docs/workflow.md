# Workflow

This is the standard workflow for paper reading, reproduction, and experiment tasks in this repository.

## New Experiment Checklist

1. Create a new folder from `shared/templates/experiment`.
2. Fill `README.md` with the experiment goal, data source, code source, and run commands.
3. Fill `paper-notes.md` using the six-part paper reading format.
4. Log every run or meaningful analysis in `reproduction-log.md`.
5. Put stable metric summaries in `results/metrics.md`.
6. Put focused result notes in files such as `results/error-analysis.md`, `results/hard-samples-*.md`, or `results/*-comparison.md`.
7. Add README links for important result files.
8. Commit only code, configs, notes, logs, and small result images.

## Six-Part Paper Notes

Every paper note should include:

1. One-sentence summary
2. Problem solved
3. Core method / workflow
4. Experiment setup
5. Limitations
6. What I can change

## Experiment Logging Rule

Every meaningful run or analysis must record an entry in `reproduction-log.md`.

The entry should include:

- date
- goal
- environment, if relevant
- command, if a command was run
- config changes
- output folder or generated files
- result metrics, if any
- problems
- fixes
- conclusion
- next step

If no command was run, still record what was analyzed and which files were created.

Quick rule:

- If an experiment creates or changes a result file, it must also update `reproduction-log.md`.

## YOLO Run Fields

For YOLO experiments, record at least:

- `data`
- `model`
- `epochs`
- `imgsz`
- `batch`
- `device`
- `project`
- `name`
- `split`, if it is validation or test

## Local Storage Rule

Keep the Git repository small. Large experiment assets should live on `D:\science-data`.

```text
D:\science-data\
|- datasets\     # downloaded datasets
|- runs\         # training outputs
`- weights\      # model weights
```

Default paths:

- datasets: `D:\science-data\datasets\<dataset-name>`
- training runs: `D:\science-data\runs\<experiment-name>`
- weights: `D:\science-data\weights`

GitHub stores code, configs, notes, logs, and small result figures only.

## Git Check Before Commit

Before committing, check:

```bash
git status --short
git diff
python .github/scripts/check_workflow.py HEAD~1 HEAD
```

Confirm that:

- `reproduction-log.md` is updated
- result notes are updated
- README links are updated when needed
- large data, weights, and full run folders are not included

## GitHub Actions Workflow Check

This repository uses `.github/workflows/check-workflow.yml` to check whether commits follow this workflow.

The check currently enforces:

- If `papers/<experiment>/configs/`, `results/`, or `scripts/` changes, then `papers/<experiment>/reproduction-log.md` must also change.
- A new experiment folder should include `README.md`, `paper-notes.md`, `reproduction-log.md`, and `results/metrics.md`.
- Large artifacts, model weights, and archive files should not be committed.

The check is intentionally focused on the most common mistakes. It does not prove that the experiment is correct; it only checks whether the basic workflow was followed.

## Known Workflow Mistake

In the first YOLO experiment, `results/hard-samples-yolov8s.md` and its figures were created, but the matching `reproduction-log.md` entry was missed.

This was not because the rule was missing. The old workflow already said to log every run in `reproduction-log.md`.

The actual error was execution failure: the existing workflow file was not checked before finishing the analysis, and the commit was made after updating result files without verifying that `reproduction-log.md` changed too.
