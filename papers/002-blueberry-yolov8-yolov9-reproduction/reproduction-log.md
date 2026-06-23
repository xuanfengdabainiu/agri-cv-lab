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
- Inspect the dataset file structure and label formats.
- Create a YOLO `data.yaml`.
- Run a 1-epoch smoke test with YOLOv8n.
- Then run a YOLOv8n baseline.

Notes:

- This project starts as a simplified reproduction. The paper reports high-resolution YOLOv8l/YOLOv9-c experiments, but the first local baseline should be smaller and cheaper.
- Large files must stay on D drive and should not be committed to Git.
