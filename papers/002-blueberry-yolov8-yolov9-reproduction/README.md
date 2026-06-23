# Blueberry YOLOv8/YOLOv9 Reproduction

## Goal

Reproduce a simplified version of the paper **Canopy Image-based Blueberry Detection by YOLOv8 and YOLOv9**.

The first goal is not to match the highest reported score immediately. The first goal is to build a clean reproduction workflow:

- download the public dataset
- inspect label format
- convert or configure data for YOLO
- run a small YOLO baseline
- evaluate detection and counting results
- write error analysis and experiment summary

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

| Run | Model | Epochs | Image Size | Purpose |
|---|---|---:|---:|---|
| smoke-yolov8n-640 | YOLOv8n | 1 | 640 | Check dataset config and training command. |
| baseline-yolov8n-640 | YOLOv8n | 50 | 640 | Small baseline. |
| baseline-yolov8s-640 | YOLOv8s | 50 | 640 | Compare with larger model. |

The paper reports high-resolution experiments such as 2560 and 3520 image size, but this reproduction will start from 640 to keep the first run manageable.

## Local Paths

- Dataset: `D:\science-data\datasets\blueberry-dcm`
- Runs: `D:\science-data\runs\blueberry-yolov8-yolov9-reproduction`
- Weights: `D:\science-data\weights`

## Notes

- This experiment starts from a simplified reproduction.
- The first technical task is to inspect the Zenodo dataset files and decide whether labels can be used directly by Ultralytics YOLO.
- If conversion is needed, conversion scripts should be placed in `scripts/`.
- Every run or analysis must be recorded in `reproduction-log.md`.
