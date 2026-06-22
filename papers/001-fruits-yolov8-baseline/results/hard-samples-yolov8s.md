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
| YOLOv8s | 20 | 0.515 | 0.408 | 0.414 | 0.266 |

The main issue is still limited Recall and imperfect localization. Precision is also not high, meaning the model still has false positives.

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

YOLOv8s is larger than YOLOv8n, but it only trained for 20 epochs. It may not have trained long enough.

More importantly, some errors seem caused by the dataset:

- image styles are mixed
- label styles are inconsistent
- some images contain printed or decorative fruit-like objects
- some scenes are cluttered or far away

Because of these issues, simply using a larger model may not solve the main problem.

## Current Conclusion

YOLOv8s can detect many obvious fruits, but the hard samples show that the main bottleneck is not only model size. The dataset and labels are also important. Before trying many model changes, it may be useful to inspect the dataset quality and define a cleaner agricultural detection subset.

## Next Step Ideas

1. Continue YOLOv8s to 50 epochs for a fairer model-size comparison.
2. Lower prediction confidence from `0.25` to `0.15` and check whether Recall improves.
3. Create a small hard-sample list with image filenames and error types.
4. Build a cleaner subset containing only real fruit photos, then retrain YOLOv8n or YOLOv8s.
5. Write a Python script to compare labels and predictions more systematically.
