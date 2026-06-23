# Error Analysis

## Purpose

This file is the final error analysis for the Fruits Detection YOLOv8 baseline experiment. It summarizes the main errors after three runs:

- YOLOv8n 50 epochs
- YOLOv8s 20 epochs
- YOLOv8s 50 epochs

The goal is to understand why the models still make mistakes, not only compare metric numbers.

## Final Compared Runs

| Run | Model | Epochs | Split | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---:|---|---:|---:|---:|---:|
| `baseline-yolov8n-640-e50-b8-v2` | YOLOv8n | 50 | test | 0.527 | 0.415 | 0.408 | 0.269 |
| `compare-yolov8s-640-e20-b8` | YOLOv8s | 20 | test | 0.515 | 0.408 | 0.414 | 0.266 |
| `compare-yolov8s-640-e50-b8-v2` | YOLOv8s | 50 | test | 0.542 | 0.438 | 0.439 | 0.294 |

YOLOv8s 50 epochs is the best run in this experiment. It improves all four test metrics compared with YOLOv8n 50 epochs, but the improvement is moderate.

## Visual Evidence

| Analysis | File |
|---|---|
| YOLOv8n hard samples | `results/hard-samples-yolov8n.md` |
| YOLOv8s 20-epoch hard samples | `results/hard-samples-yolov8s.md` |
| YOLOv8s 50-epoch hard samples | `results/hard-samples-yolov8s-e50.md` |
| YOLOv8n vs YOLOv8s comparison | `results/yolov8n-vs-yolov8s-comparison.md` |

Representative figures are stored in `results/figures/`.

## Main Error Types

### 1. Missed Objects in Dense or Cluttered Scenes

Recall is still not high even in the best run:

- YOLOv8s 50 epochs Recall: 0.438

This means many real fruits are still missed. The problem is common in:

- dense apple scenes
- grape clusters
- market scenes
- fruits that are small, far away, or partly hidden

### 2. Group Box vs Individual Box Mismatch

The dataset has inconsistent annotation styles. Some images label a whole fruit group with one large box, while other images label individual fruits separately.

This causes a difficult situation:

- If the model predicts many small boxes, it may look visually reasonable but score poorly when the label is one group box.
- If the model predicts one large box, it may match some labels but miss individual fruit detail.

This affects both YOLOv8n and YOLOv8s.

### 3. False Positives on Printed, Painted, or Decorative Objects

The dataset contains images that are not clean real-fruit detection scenes. Some examples include:

- printed fruit images
- paintings containing fruit-like objects
- decorative fruit-shaped objects
- market signs or background patterns

The model sometimes detects these as real fruit. This lowers Precision.

### 4. Class Confusion

Some fruit classes are confused in unusual scenes. Pineapple, grape, orange, apple, and banana can be confused when:

- the object is small
- the object is partly hidden
- the image style is unusual
- the object is decorative or printed

Watermelon is relatively distinctive, while orange and pineapple remain harder.

### 5. Dataset Style Is Too Mixed

The dataset is useful for learning the YOLO workflow, but it mixes many image types:

- clean product photos
- farm or natural scenes
- market scenes
- paintings
- printed images
- decorative objects

This makes the task less like a clean agricultural detection dataset.

## What Improved After YOLOv8s 50 Epochs

Compared with YOLOv8s 20 epochs, YOLOv8s 50 epochs improved:

- Precision: 0.515 to 0.542
- Recall: 0.408 to 0.438
- mAP50: 0.414 to 0.439
- mAP50-95: 0.266 to 0.294

Visually, the 50-epoch model is often more conservative and produces fewer noisy boxes. This helps, but it does not remove the main dataset-related errors.

## Final Error Conclusion

The main bottleneck is no longer simply "the model is too small." YOLOv8s 50 epochs performs better than YOLOv8n 50 epochs, so model size and training length do help.

However, the remaining errors strongly suggest that dataset quality and label consistency are the bigger next problem. Continuing to try larger models may give small improvements, but the more useful next step is likely data cleaning.

## Recommended Next Direction

End this experiment here and start a new experiment focused on data quality:

1. Build a cleaner real-fruit subset.
2. Remove or separate paintings, printed images, decorative objects, and confusing market signs.
3. Check whether labels use group boxes or individual boxes.
4. Retrain YOLOv8n or YOLOv8s on the cleaner subset.
5. Compare original dataset vs cleaned subset.
