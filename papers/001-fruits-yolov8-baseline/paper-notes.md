# Notes

## 1. One-Sentence Summary

This is not a paper reproduction; it is a YOLOv8 baseline experiment on a public fruit detection dataset.

## 2. Problem Solved

Learn the full object detection workflow before reproducing a more complex agricultural detection paper.

## 3. Core Method / Workflow

```text
Public YOLO-format fruit dataset
  ↓
Ultralytics YOLOv8 baseline training
  ↓
Validation metrics and prediction visualizations
```

## 4. Experiment Setup

- Dataset: lightly-ai/dataset_fruits_detection
- Baselines: YOLOv8n first; optionally YOLOv8s later
- Metrics: Precision, Recall, mAP50, mAP50-95
- Training settings: start with epochs=50, imgsz=640
- Main results: TBD

## 5. Limitations

- This is not a strict paper reproduction.
- The dataset is for practice and may not represent real orchard field conditions.
- Results should be treated as a baseline, not a publishable method.

## 6. What I Can Change

- Compare YOLOv8n and YOLOv8s.
- Try data augmentation settings.
- Add a lightweight attention module later.
- Move the learned workflow to a real agricultural dataset such as MinneApple or PlantDoc.
