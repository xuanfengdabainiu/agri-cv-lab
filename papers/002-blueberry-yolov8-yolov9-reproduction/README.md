# Blueberry YOLOv8/YOLOv9 Reproduction

## Goal

Fully reproduce the main experiments from **Canopy Image-based Blueberry Detection by YOLOv8 and YOLOv9**.

The target is to reproduce the paper's main workflow as closely as possible:

- download the public BlueberryDCM dataset
- inspect the official code and dataset split
- reproduce YOLOv8l experiments
- reproduce YOLOv9-c experiments
- test high-resolution settings such as 2560 and 3520 image size if hardware allows
- compute detection metrics
- compute fruit counting RMSE
- compute Blue fruit percentage RMSE
- compare reproduced results with the paper

## Paper

- Title: Canopy Image-based Blueberry Detection by YOLOv8 and YOLOv9
- Authors: Boyang Deng, Yuzhen Lu
- Paper URL: https://ssrn.com/abstract=4981340
- Code: https://github.com/vicdxxx/BlueberryDetectionAndCounting
- Dataset: https://zenodo.org/records/14002517

## Status

`setup`

## Why This Paper

This paper is a good next reproduction after the Fruits YOLOv8 baseline because:

- it is agricultural object detection
- it uses YOLOv8, which matches the previous experiment workflow
- it focuses on blueberries, which is close to the lab direction
- it has public code and a public dataset
- it includes detection, counting, and maturity assessment

## Dataset

Dataset name:

- BlueberryDCM

Dataset description:

- 140 RGB blueberry canopy images
- captured by smartphones in natural field light
- 17,955 bounding box annotations
- two maturity classes:
  - `Blue`: ripe blueberry
  - `Unblue`: unripe blueberry
- visibility sub-categories:
  - `visible`
  - `occluded`

Local dataset target path:

```text
D:\science-data\datasets\blueberry-dcm
```

Large dataset files should stay on D drive and should not be committed to Git.

## Planned Runs

| Run | Model | Image Size | Purpose |
|---|---|---:|---|
| inspect-dataset | - | - | Inspect official dataset structure, labels, and split. |
| reproduce-yolov8l-2560 | YOLOv8l | 2560 | Reproduce main YOLOv8l high-resolution experiment. |
| reproduce-yolov9c-2560 | YOLOv9-c | 2560 | Reproduce main YOLOv9-c high-resolution experiment. |
| reproduce-yolov8l-3520 | YOLOv8l | 3520 | Reproduce the highest-resolution YOLOv8l result if hardware allows. |

If the laptop GPU cannot fit the paper's exact settings, the reproduction log must record the limitation clearly and use the closest possible batch size or image size.

## Local Paths

- Dataset: `D:\science-data\datasets\blueberry-dcm`
- Runs: `D:\science-data\runs\blueberry-yolov8-yolov9-reproduction`
- Weights: `D:\science-data\weights`
- Official code: `D:\science-data\code\BlueberryDetectionAndCounting`
- Conda environment: `D:\conda_envs\blueberry-yolo`

## Notes

- This experiment is now planned as a full reproduction, not a simplified baseline.
- The first technical task is to inspect the Zenodo dataset files and official GitHub code to identify the exact split, label format, training parameters, and evaluation scripts.
- The environment record is stored in `configs/environment.yaml`.
- If conversion is needed, conversion scripts should be placed in `scripts/`.
- Every run or analysis must be recorded in `reproduction-log.md`.
