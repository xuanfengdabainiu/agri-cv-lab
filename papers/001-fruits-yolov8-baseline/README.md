# Fruits Detection YOLOv8 Baseline

## Goal

Train a clean Ultralytics YOLOv8 baseline on a public fruit detection dataset, then record the full workflow as the first reproducible agricultural computer vision experiment.

## Paper

- Title: No fixed paper. This is a baseline engineering reproduction.
- DOI / URL: -
- Code: Ultralytics YOLOv8
- Dataset: https://github.com/lightly-ai/dataset_fruits_detection

## Status

`baseline complete`

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
| smoke-yolov8n-320 | YOLOv8n | Fruits Detection | 0.29064 | 0.28016 | 0.18047 | 0.10253 | 1 epoch smoke test |
| baseline-yolov8n-640-e50-b8-v2 | YOLOv8n | Fruits Detection | 0.638 | 0.441 | 0.478 | 0.320 | 50 epochs, best.pt on val |
| baseline-yolov8n-640-e50-b8-v2 | YOLOv8n | Fruits Detection | 0.527 | 0.415 | 0.408 | 0.269 | 50 epochs, best.pt on test |
| compare-yolov8s-640-e20-b8 | YOLOv8s | Fruits Detection | 0.592 | 0.450 | 0.481 | 0.310 | 20 epochs, best.pt on val |
| compare-yolov8s-640-e20-b8 | YOLOv8s | Fruits Detection | 0.515 | 0.408 | 0.414 | 0.266 | 20 epochs, best.pt on test |

## Dataset

Source: https://github.com/lightly-ai/dataset_fruits_detection

Local path:

```text
D:\science-data\datasets\fruits-detection
```

Classes:

- Apple
- Banana
- Grape
- Orange
- Pineapple
- Watermelon

## Notes

- Data is stored outside Git.
- Weights and full runs are excluded from Git.
- This experiment is for learning the complete YOLO workflow: dataset setup, training, validation, prediction, metrics, and logging.
- Current experiment summary: [results/experiment-summary.md](results/experiment-summary.md)
- First test-set error analysis: [results/error-analysis.md](results/error-analysis.md)
- YOLOv8s hard-sample analysis: [results/hard-samples-yolov8s.md](results/hard-samples-yolov8s.md)

## Local Paths

- Dataset: `D:\science-data\datasets\fruits-detection`
- Runs: `D:\science-data\runs\fruits-yolov8-baseline`
- Weights: `D:\science-data\weights`
