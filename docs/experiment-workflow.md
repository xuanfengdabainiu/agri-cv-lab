# Experiment Workflow

This document is the standard workflow for future reproduction or experiment tasks in this repository.

## Why This Exists

One issue happened in the first YOLO experiment:

- The YOLOv8s hard-sample analysis file was created.
- The figures were saved.
- The README was updated.
- But `reproduction-log.md` was not updated at the same time.

The missing log made it harder to understand when and why the analysis was done.

To avoid this, every experiment should follow the checklist below.

## Standard Experiment Checklist

### 1. Before Running

Record the plan in the experiment folder:

- experiment goal
- model name
- dataset split
- important parameters, such as epochs, image size, batch size, device
- expected output folder

If the experiment is small, this can be written directly in `reproduction-log.md`.

### 2. Run the Experiment

Save the exact command.

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

### 3. Save Local Outputs

Keep large files outside Git:

- datasets
- full run folders
- trained weights
- generated prediction folders

For this repository, large files usually stay under:

```text
D:\science-data
```

### 4. Copy Small Evidence Into Git

Copy small, useful evidence into the repo:

- metric tables
- selected prediction images
- confusion matrix images
- loss or mAP curves
- short analysis notes

Do not commit large weights or full run folders.

### 5. Update the Result Notes

Depending on the task, update one or more result files:

- `results/metrics.md`
- `results/error-analysis.md`
- `results/hard-samples-*.md`
- `results/*-comparison.md`
- `results/experiment-summary.md`

The note should include:

- what was tested
- which model and weights were used
- which dataset split was used
- where the local output is stored
- main metrics
- main observation
- current conclusion
- next step

### 6. Update `reproduction-log.md`

This step is required.

Every meaningful experiment or analysis must add an entry to `reproduction-log.md`.

The entry should include:

- date
- goal
- command, if a command was run
- output folder or generated files
- result numbers, if any
- notes or conclusion
- next step

If no command was run, still record what was analyzed and which files were created.

### 7. Update Index Files

If a new important result file is created, add a link from:

- the experiment `README.md`
- `reproduction-log.md`

This makes the file easier to find later.

### 8. Check Git Diff

Before committing, check:

```bash
git status --short
git diff
```

Confirm that:

- code/config/result notes are included
- `reproduction-log.md` is updated
- README links are updated when needed
- large data, weights, and run folders are not accidentally included

### 9. Commit and Push

Use a clear commit message, such as:

```bash
git commit -m "Record YOLOv8s hard sample analysis"
git push
```

### 10. Final Response to User

Tell the user:

- what was done
- which files were changed
- where local outputs are stored
- whether GitHub was updated
- what the next step is

## Quick Rule

If an experiment creates or changes a result file, it must also update `reproduction-log.md`.
