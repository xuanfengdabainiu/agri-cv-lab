# Experiment Summary

## Purpose

This experiment is the first complete agricultural computer vision practice in this repository. The goal was not to propose a new algorithm, but to learn and record a full YOLO object detection workflow:

- set up the environment
- prepare a dataset
- train baseline models
- validate and test trained weights
- compare model sizes
- inspect prediction errors
- keep reproducible experiment records

The task is fruit detection with six classes:

- Apple
- Banana
- Grape
- Orange
- Pineapple
- Watermelon

## Dataset

Dataset:

- Fruits Detection dataset
- Local path: `D:\science-data\datasets\fruits-detection`

The dataset is useful for learning YOLO, but it is visually mixed. It contains clean fruit photos, market scenes, product-like images, paintings, printed fruit-like objects, and decorative objects.

## Environment

- Conda environment: `D:\conda_envs\agri-yolo`
- Main tool: Ultralytics YOLOv8
- GPU: NVIDIA GeForce RTX 5060 Laptop GPU
- Large local outputs: `D:\science-data\runs\fruits-yolov8-baseline`

## Completed Runs

### 1. Smoke Test

- Run: `smoke-yolov8n-320`
- Model: YOLOv8n
- Epochs: 1
- Image size: 320
- Purpose: check whether the environment, dataset config, and training command work.

### 2. YOLOv8n Baseline

- Run: `baseline-yolov8n-640-e50-b8-v2`
- Model: YOLOv8n
- Epochs: 50
- Image size: 640
- Batch size: 8
- Best weights: `D:\science-data\runs\fruits-yolov8-baseline\baseline-yolov8n-640-e50-b8-v2\weights\best.pt`

This is the main small-model baseline.

### 3. YOLOv8s Quick Compare

- Run: `compare-yolov8s-640-e20-b8`
- Model: YOLOv8s
- Epochs: 20
- Image size: 640
- Batch size: 8
- Best weights: `D:\science-data\runs\fruits-yolov8-baseline\compare-yolov8s-640-e20-b8\weights\best.pt`

This run was used as an early check. It was not a fair final comparison because YOLOv8n trained for 50 epochs while YOLOv8s trained for only 20 epochs.

### 4. YOLOv8s Fair Comparison

- Run: `compare-yolov8s-640-e50-b8-v2`
- Model: YOLOv8s
- Epochs: 50
- Image size: 640
- Batch size: 8
- Best weights: `D:\science-data\runs\fruits-yolov8-baseline\compare-yolov8s-640-e50-b8-v2\weights\best.pt`

This is the fairer comparison with YOLOv8n because both models trained for 50 epochs.

## Final Results

### Validation Set

| Model | Epochs | Precision | Recall | mAP50 | mAP50-95 |
|---|---:|---:|---:|---:|---:|
| YOLOv8n | 50 | 0.638 | 0.441 | 0.478 | 0.320 |
| YOLOv8s | 20 | 0.592 | 0.450 | 0.481 | 0.310 |
| YOLOv8s | 50 | 0.638 | 0.474 | 0.496 | 0.332 |

### Test Set

| Model | Epochs | Precision | Recall | mAP50 | mAP50-95 |
|---|---:|---:|---:|---:|---:|
| YOLOv8n | 50 | 0.527 | 0.415 | 0.408 | 0.269 |
| YOLOv8s | 20 | 0.515 | 0.408 | 0.414 | 0.266 |
| YOLOv8s | 50 | 0.542 | 0.438 | 0.439 | 0.294 |

## What The Metrics Mean

- Precision: among predicted boxes, how many are correct. Higher Precision means fewer false detections.
- Recall: among real objects, how many are found. Higher Recall means fewer missed objects.
- mAP50: a common detection score using a looser box-matching standard.
- mAP50-95: a stricter detection score. It requires boxes to be more accurately located.

## Main Findings

### 1. The Full YOLO Workflow Was Completed

This experiment successfully covered:

- dataset setup
- training
- validation
- test evaluation
- prediction image inspection
- metrics recording
- hard-sample analysis
- GitHub logging
- workflow check with GitHub Actions

### 2. YOLOv8s 50 Epochs Is The Best Run

YOLOv8s 50 epochs improves all four test metrics compared with YOLOv8n 50 epochs:

- Precision: 0.527 to 0.542
- Recall: 0.415 to 0.438
- mAP50: 0.408 to 0.439
- mAP50-95: 0.269 to 0.294

This shows that a larger model and longer training help.

### 3. The Improvement Is Moderate

YOLOv8s 50 epochs is better, but the improvement is not large enough to say the task is solved. The best test Recall is still only 0.438, meaning missed detections are still common.

### 4. Dataset Quality Is The Main Next Bottleneck

Hard-sample analysis shows repeated issues:

- mixed image styles
- decorative or printed fruit-like objects
- paintings and non-real fruit scenes
- cluttered market scenes
- inconsistent group-box vs individual-box labels

These issues affect both YOLOv8n and YOLOv8s.

### 5. The Experiment Record System Improved

During this experiment, a missing `reproduction-log.md` entry was found and fixed. A GitHub Actions workflow check was added to prevent the same mistake:

- If `configs/`, `results/`, or `scripts/` changes, `reproduction-log.md` must also change.

## Final Conclusion

This experiment can be closed.

The best result is YOLOv8s trained for 50 epochs:

- Precision: 0.542
- Recall: 0.438
- mAP50: 0.439
- mAP50-95: 0.294

The final conclusion is:

> YOLOv8s 50 epochs is better than YOLOv8n 50 epochs on this fruit detection dataset, but the improvement is moderate. The next meaningful improvement should focus on data cleaning and label consistency, not only trying larger models.

## Final Files

Important result files:

- `results/metrics.md`
- `results/error-analysis.md`
- `results/hard-samples-yolov8n.md`
- `results/hard-samples-yolov8s.md`
- `results/hard-samples-yolov8s-e50.md`
- `results/yolov8n-vs-yolov8s-comparison.md`
- `reproduction-log.md`

## Recommended Next Experiment

Start a new experiment focused on data quality:

1. Create a cleaner real-fruit subset.
2. Remove or separate paintings, printed images, decorative objects, and confusing market signs.
3. Decide whether labels should be group boxes or individual fruit boxes.
4. Retrain YOLOv8n or YOLOv8s on the cleaned subset.
5. Compare original dataset vs cleaned subset.
