# YOLOv8n Hard Samples

## Purpose

This note analyzes hard test samples for the YOLOv8n baseline model. It is used as a comparison reference for the YOLOv8s hard-sample analysis.

## Model Files

Original pretrained model file:

- YOLOv8n pretrained file: `C:\Users\liuqilu\Documents\science\agri-cv-lab\yolov8n.pt`

Trained model file:

- YOLOv8n trained best weights: `D:\science-data\runs\fruits-yolov8-baseline\baseline-yolov8n-640-e50-b8-v2\weights\best.pt`

The pretrained `.pt` file is the starting point. The `best.pt` file is the model trained on this fruit dataset.

## Run

- Model: YOLOv8n
- Epochs: 50
- Weights: `D:\science-data\runs\fruits-yolov8-baseline\baseline-yolov8n-640-e50-b8-v2\weights\best.pt`
- Dataset split: test
- Test validation output: `D:\science-data\runs\fruits-yolov8-baseline\baseline-yolov8n-640-e50-b8-v2-val-test-rerun`

## Test Metrics

| Model | Epochs | Precision | Recall | mAP50 | mAP50-95 |
|---|---:|---:|---:|---:|---:|
| YOLOv8n | 50 | 0.527 | 0.415 | 0.408 | 0.269 |

The main weakness is Recall. This means the model still misses many true objects. Precision is also limited, meaning some predicted boxes are false positives.

## Visual Samples

| Sample | Ground Truth | Prediction | Main Problem |
|---|---|---|---|
| Batch 0 | `figures/test-batch0-labels.jpg` | `figures/test-batch0-pred.jpg` | Dense fruit scenes, printed fruit-like objects, and group-vs-instance label mismatch. |
| Batch 1 | `figures/test-batch1-labels.jpg` | `figures/test-batch1-pred.jpg` | False positives on non-fruit or decorative objects, plus class confusion. |
| Batch 2 | `figures/test-batch2-labels.jpg` | `figures/test-batch2-pred.jpg` | Market scenes, paintings, decorations, and cluttered backgrounds. |

## Observed Error Types

### 1. Dense Fruit Scenes

In dense apple, orange, banana, and grape images, YOLOv8n sometimes predicts only part of the fruits or produces several small boxes. This becomes difficult when the label style is not consistent.

Example:

- In Batch 0, apple and orange scenes contain many fruits, but the predictions and labels do not always use the same box style.

### 2. Group Box vs Instance Box Mismatch

Some images use one large box for a whole group of fruits. Other images use separate boxes for individual fruits. YOLOv8n may predict individual fruits while the label expects one group box, or the opposite.

This hurts the metric even when the visual prediction looks partly reasonable.

### 3. False Positives on Non-Fruit Objects

YOLOv8n sometimes predicts fruit labels on objects that only look similar to fruits, including decorations, printed images, drawings, and background objects.

Examples:

- In Batch 0, a printed apple-like shape on a book cover is detected as Apple.
- In Batch 1, decorative or non-real objects are detected as fruit.
- In Batch 2, paintings and market decorations create confusing visual patterns.

This lowers Precision.

### 4. Missed Objects

YOLOv8n misses some real fruits, especially when the fruit is small, partially occluded, far away, or surrounded by clutter.

This lowers Recall.

### 5. Class Confusion

YOLOv8n sometimes confuses visually similar categories or unusual appearances. For example, fruit decorations or unusual pineapple, grape, orange, and banana scenes can cause wrong class predictions.

## Comparison With YOLOv8s Hard Samples

The YOLOv8n hard samples show similar problem types to YOLOv8s:

- mixed image styles
- inconsistent group-vs-instance labels
- printed, painted, or decorative fruit-like objects
- cluttered scenes and small objects
- class confusion between visually similar fruit categories

This makes the YOLOv8s conclusion more careful: the current evidence does not show that YOLOv8s clearly solves the problem. Some errors are shared by both models and are related to dataset quality or label style, not only model size.

## Current Conclusion

YOLOv8n gives a useful baseline, but its hard samples show clear limits. The next improvement should not only be "use a bigger model"; it should also include dataset inspection, label cleaning, and a fairer YOLOv8n-vs-YOLOv8s training comparison.

## Next Step Ideas

1. Compare the same Batch 0, Batch 1, and Batch 2 images between YOLOv8n and YOLOv8s.
2. Make a small table of repeated error types shared by both models.
3. Create a cleaner subset with real fruit photos only.
4. Train YOLOv8s for 50 epochs to make the model-size comparison fairer.
