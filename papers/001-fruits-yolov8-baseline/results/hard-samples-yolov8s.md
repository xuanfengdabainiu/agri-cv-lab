# YOLOv8s Hard Samples

## Purpose

This note analyzes hard test samples for the YOLOv8s quick-compare model. The goal is to understand what kinds of images are difficult for the model, instead of only looking at metric numbers.

## Model Files

Original pretrained model files:

- YOLOv8n pretrained file: `C:\Users\liuqilu\Documents\science\agri-cv-lab\yolov8n.pt`
- YOLOv8s pretrained file: `C:\Users\liuqilu\Documents\science\agri-cv-lab\yolov8s.pt`

Trained model files:

- YOLOv8n trained best weights: `D:\science-data\runs\fruits-yolov8-baseline\baseline-yolov8n-640-e50-b8-v2\weights\best.pt`
- YOLOv8s trained best weights: `D:\science-data\runs\fruits-yolov8-baseline\compare-yolov8s-640-e20-b8\weights\best.pt`

The pretrained `.pt` files are starting points. The `best.pt` files are the weights trained on this fruit dataset.

## Run

- Model: YOLOv8s
- Epochs: 20
- Weights: `D:\science-data\runs\fruits-yolov8-baseline\compare-yolov8s-640-e20-b8\weights\best.pt`
- Dataset split: test
- Prediction output: `D:\science-data\runs\fruits-yolov8-baseline\compare-yolov8s-640-e20-b8-predict-test`
- Test validation output: `D:\science-data\runs\fruits-yolov8-baseline\compare-yolov8s-640-e20-b8-val-test`

## Test Metrics

| Model | Epochs | Precision | Recall | mAP50 | mAP50-95 |
|---|---:|---:|---:|---:|---:|
| YOLOv8n | 50 | 0.527 | 0.415 | 0.408 | 0.269 |
| YOLOv8s | 20 | 0.515 | 0.408 | 0.414 | 0.266 |

The YOLOv8n result was rerun on the test split and matched the previous record. YOLOv8s only improves mAP50 slightly, while Precision, Recall, and mAP50-95 are slightly lower. This is not enough to conclude that YOLOv8s is better.

## Visual Samples

| Sample | Ground Truth | Prediction | Main Problem |
|---|---|---|---|
| Batch 0 | `figures/yolov8s-hard-batch0-labels.jpg` | `figures/yolov8s-hard-batch0-pred.jpg` | Dense fruit scenes and inconsistent group-vs-instance boxes. |
| Batch 1 | `figures/yolov8s-hard-batch1-labels.jpg` | `figures/yolov8s-hard-batch1-pred.jpg` | False positives on non-fruit regions and partial detections of grapes/oranges. |
| Batch 2 | `figures/yolov8s-hard-batch2-labels.jpg` | `figures/yolov8s-hard-batch2-pred.jpg` | Mixed image types, such as market scenes, paintings, and decorative fruit-like objects. |

## Observed Error Types

### 1. Dense Fruit Scenes

In dense apple, orange, and grape images, the model often predicts many small boxes. Sometimes this is visually reasonable, but the dataset label may use one large group box or only a few boxes. This mismatch hurts the metric score.

Example:

- In Batch 0, the apple scene contains many apples. YOLOv8s predicts many apple boxes, while the label style is not always one-box-per-fruit.

### 2. Group Box vs Instance Box Mismatch

Some images label a whole group of fruits with one large box. Other images label individual fruits separately. The model is not sure whether it should predict one large box or multiple small boxes.

This is a dataset-labeling issue, not only a model issue.

### 3. False Positives

YOLOv8s sometimes detects non-fruit objects as fruit. For example, background regions, objects shaped like fruits, or printed/decorative fruit-like patterns may be predicted as Apple, Banana, Orange, Pineapple, or Watermelon.

This lowers Precision.

### 4. Missed Objects

Some real fruits are not detected, especially when they are small, partly hidden, or located in cluttered backgrounds.

This lowers Recall.

### 5. Class Confusion

The model sometimes confuses visually similar or unusual fruit appearances. Pineapple, Grape, Orange, and Apple can be confused when the image is unusual or the object is small.

## Why YOLOv8s Did Not Clearly Beat YOLOv8n

The YOLOv8n test result was rerun and confirmed:

- YOLOv8n 50 epochs: Precision 0.527, Recall 0.415, mAP50 0.408, mAP50-95 0.269
- YOLOv8s 20 epochs: Precision 0.515, Recall 0.408, mAP50 0.414, mAP50-95 0.266

So YOLOv8s only improves mAP50 slightly, while the other three metrics are slightly lower. This is not enough to conclude that YOLOv8s is better.

This comparison is also not fully fair because YOLOv8n trained for 50 epochs and YOLOv8s trained for 20 epochs. YOLOv8s may need longer training.

The hard-sample images suggest that both model size and data quality may matter. The dataset contains:

- image styles are mixed
- label styles are inconsistent
- some images contain printed or decorative fruit-like objects
- some scenes are cluttered or far away

These issues can affect both YOLOv8n and YOLOv8s, so simply increasing model size may not be sufficient.

## Current Conclusion

YOLOv8s can detect many obvious fruits, but based on the YOLOv8n rerun and YOLOv8s test result, YOLOv8s 20 epochs is not clearly better. The current evidence suggests that training length and dataset quality should both be checked before concluding that a larger model helps.

## Next Step Ideas

1. Continue YOLOv8s to 50 epochs for a fairer model-size comparison.
2. Lower prediction confidence from `0.25` to `0.15` and check whether Recall improves.
3. Create a small hard-sample list with image filenames and error types.
4. Build a cleaner subset containing only real fruit photos, then retrain YOLOv8n or YOLOv8s.
5. Write a Python script to compare labels and predictions more systematically.
