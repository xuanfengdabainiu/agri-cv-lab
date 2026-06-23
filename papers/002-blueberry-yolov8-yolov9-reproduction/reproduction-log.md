# Reproduction Log

## 2026-06-23 Project Setup

Goal:

- Create a new reproduction project for **Canopy Image-based Blueberry Detection by YOLOv8 and YOLOv9**.
- Follow the same project structure used by the first Fruits YOLOv8 baseline experiment.

Sources:

- Paper: https://ssrn.com/abstract=4981340
- Code: https://github.com/vicdxxx/BlueberryDetectionAndCounting
- Dataset: https://zenodo.org/records/14002517

What was created:

- `README.md`
- `paper-notes.md`
- `reproduction-log.md`
- `configs/`
- `scripts/`
- `results/`
- `results/metrics.md`
- `results/figures/`

Initial plan:

- Download the BlueberryDCM dataset to `D:\science-data\datasets\blueberry-dcm`.
- Download or inspect the official GitHub code.
- Identify the exact dataset split, label format, training parameters, and evaluation scripts.
- Reproduce YOLOv8l experiments.
- Reproduce YOLOv9-c experiments.
- Compute detection mAP, counting RMSE, and Blue fruit percentage RMSE.

Notes:

- This project is planned as a full reproduction of the paper's main experiments.
- Large files must stay on D drive and should not be committed to Git.

## 2026-06-23 Plan Updated to Full Reproduction

Reason:

- The project should target full paper reproduction, not a simplified beginner baseline.

Updated plan:

- Reproduce YOLOv8l and YOLOv9-c experiments from the paper.
- Use the paper's high-resolution settings such as 2560 and 3520 image size when hardware allows.
- Record any hardware-driven changes, such as smaller batch size.
- Compute both detection metrics and application metrics:
  - mAP
  - fruit counting RMSE
  - Blue fruit percentage RMSE

Immediate next step:

- Download the BlueberryDCM dataset and official code to D drive.
- Inspect the official file structure before writing configs or commands.
