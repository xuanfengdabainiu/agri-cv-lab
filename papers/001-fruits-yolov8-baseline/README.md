# Fruits Detection YOLOv8 Baseline

## Goal

Train a clean Ultralytics YOLOv8 baseline on a public fruit detection dataset, then record the full workflow as the first reproducible agricultural computer vision experiment.

## Paper

- Title: No fixed paper. This is a baseline engineering reproduction.
- DOI / URL: -
- Code: Ultralytics YOLOv8
- Dataset: https://github.com/lightly-ai/dataset_fruits_detection

## Status

`setup`

## Quick Start

```bash
conda env create -f envs/yolo-env.yml
conda activate agri-yolo
yolo detect train data=papers/001-fruits-yolov8-baseline/configs/data.yaml model=yolov8n.pt epochs=50 imgsz=640
```

## Main Results

| Run | Model | Dataset | Precision | Recall | mAP50 | mAP50-95 | Notes |
|---|---|---|---:|---:|---:|---:|---|
| baseline-001 | YOLOv8n | Fruits Detection | - | - | - | - | planned |

## Notes

- Data is stored outside Git.
- Weights and full runs are excluded from Git.
- This experiment is for learning the complete YOLO workflow: dataset setup, training, validation, prediction, metrics, and logging.

## Local Paths

- Dataset: `D:\science-data\datasets\fruits-detection`
- Runs: `D:\science-data\runs\fruits-yolov8-baseline`
- Weights: `D:\science-data\weights`
