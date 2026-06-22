# YOLOv8n vs YOLOv8s Comparison

## Purpose

This note compares YOLOv8n and YOLOv8s on the same fruit detection test split. The goal is to check whether the larger YOLOv8s model clearly improves over the smaller YOLOv8n baseline.

## Compared Runs

| Model | Epochs | Weights | Test Output |
|---|---:|---|---|
| YOLOv8n | 50 | `D:\science-data\runs\fruits-yolov8-baseline\baseline-yolov8n-640-e50-b8-v2\weights\best.pt` | `D:\science-data\runs\fruits-yolov8-baseline\baseline-yolov8n-640-e50-b8-v2-val-test-rerun` |
| YOLOv8s | 20 | `D:\science-data\runs\fruits-yolov8-baseline\compare-yolov8s-640-e20-b8\weights\best.pt` | `D:\science-data\runs\fruits-yolov8-baseline\compare-yolov8s-640-e20-b8-val-test` |

Important note: this is not a fully fair comparison because YOLOv8n trained for 50 epochs, while YOLOv8s trained for 20 epochs.

## Test Metrics

| Model | Epochs | Precision | Recall | mAP50 | mAP50-95 |
|---|---:|---:|---:|---:|---:|
| YOLOv8n | 50 | 0.527 | 0.415 | 0.408 | 0.269 |
| YOLOv8s | 20 | 0.515 | 0.408 | 0.414 | 0.266 |

Simple reading:

- YOLOv8s has slightly higher mAP50.
- YOLOv8n has slightly higher Precision, Recall, and mAP50-95.
- The difference is small, so YOLOv8s is not clearly better in this setting.

## Same-Batch Visual Comparison

| Batch | Ground Truth | YOLOv8n Prediction | YOLOv8s Prediction |
|---|---|---|---|
| Batch 0 | `figures/test-batch0-labels.jpg` | `figures/test-batch0-pred.jpg` | `figures/yolov8s-hard-batch0-pred.jpg` |
| Batch 1 | `figures/test-batch1-labels.jpg` | `figures/test-batch1-pred.jpg` | `figures/yolov8s-hard-batch1-pred.jpg` |
| Batch 2 | `figures/test-batch2-labels.jpg` | `figures/test-batch2-pred.jpg` | `figures/yolov8s-hard-batch2-pred.jpg` |

## Main Observations

### 1. Both Models Struggle With Mixed Image Styles

The test set contains real fruit photos, market scenes, decorative objects, printed fruit-like patterns, and paintings. Both models can make mistakes on these mixed styles.

Examples:

- Printed apple-like shapes may be detected as Apple.
- Decorative grape or fruit-like objects may be detected as Grape or Pineapple.
- Paintings containing fruit-like objects may trigger false positives.

This suggests that part of the problem comes from dataset style, not only model size.

### 2. YOLOv8s Predicts More Boxes in Some Dense Scenes

In dense apple and orange scenes, YOLOv8s often predicts more individual boxes than YOLOv8n.

This can be helpful when the label uses one box per fruit. But it can hurt the metric when the label uses one large group box for many fruits.

So "more boxes" is not always better. It depends on whether the dataset labels expect individual-object boxes or group boxes.

### 3. YOLOv8n Is Sometimes More Conservative

YOLOv8n often predicts fewer boxes in dense or confusing images. This can reduce some false positives, but it can also miss real fruits.

This matches the metrics:

- YOLOv8n has slightly higher Precision than YOLOv8s.
- YOLOv8n also has slightly higher Recall in this test result, but both Recall values are low.

### 4. Both Models Have False Positives

Both YOLOv8n and YOLOv8s detect some non-fruit regions as fruit.

Common false-positive causes:

- printed fruit pictures
- decorative fruit-like objects
- confusing background textures
- unusual fruit-shaped objects

This affects Precision.

### 5. Both Models Miss Objects

Both models miss fruits when the objects are small, occluded, far away, or in cluttered backgrounds.

This affects Recall.

### 6. Label Inconsistency Makes the Comparison Harder

Some images are labeled with one big box around a group of fruits. Other images are labeled with many small boxes for individual fruits.

This makes the model behavior hard to judge:

- A model predicting many small boxes may look reasonable visually.
- But if the ground truth uses one group box, the metric may punish it.
- A model predicting one big box may look coarse.
- But if the ground truth also uses one group box, the metric may reward it.

This is why visual analysis is important together with metric analysis.

## Current Conclusion

YOLOv8s 20 epochs does not clearly beat YOLOv8n 50 epochs on the test split. It only slightly improves mAP50, while Precision, Recall, and mAP50-95 are slightly lower.

The visual comparison shows that both models share similar hard cases. The main bottleneck is likely a combination of:

- YOLOv8s training time may be insufficient
- dataset image styles are mixed
- labels are not fully consistent
- some samples are not clean real-fruit detection images

So the current conclusion should be careful:

> Under the current settings, YOLOv8s is not clearly better than YOLOv8n. More training and cleaner data are both worth checking before changing the model structure.

## Next Step

The best next experiment is to train YOLOv8s for 50 epochs. This will make the model-size comparison fairer because both YOLOv8n and YOLOv8s would use the same epoch setting.

After that, compare:

- YOLOv8n 50 epochs on test
- YOLOv8s 50 epochs on test
- hard samples from both models
