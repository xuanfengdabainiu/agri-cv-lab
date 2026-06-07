# Workflow

## New Experiment Checklist

1. Create a new folder from `shared/templates/experiment`.
2. Fill `README.md` with the experiment goal, data source, code source, and run commands.
3. Fill `paper-notes.md` using the six-part paper reading format.
4. Log every run in `reproduction-log.md`.
5. Put stable metric summaries in `results/metrics.md`.
6. Commit only code, configs, notes, and small result images.

## Six-Part Paper Notes

Every paper note should include:

1. One-sentence summary
2. Problem solved
3. Core method / workflow
4. Experiment setup
5. Limitations
6. What I can change

## Experiment Logging Rule

Every meaningful run should record:

- date
- goal
- environment
- command
- config changes
- result metrics
- problems
- fixes
- next step

## Local Storage Rule

Keep the Git repository small. Large experiment assets should live on `D:\science-data`.

```text
D:\science-data\
├─ datasets\     # downloaded datasets
├─ runs\         # training outputs
└─ weights\      # model weights
```

Default paths:

- datasets: `D:\science-data\datasets\<dataset-name>`
- training runs: `D:\science-data\runs\<experiment-name>`
- weights: `D:\science-data\weights`

GitHub stores code, configs, notes, logs, and small result figures only.
