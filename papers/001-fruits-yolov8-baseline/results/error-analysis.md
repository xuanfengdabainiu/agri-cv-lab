# Error Analysis

## Run

- Date: 2026-06-21
- Model: YOLOv8n
- Weights: `D:\science-data\runs\fruits-yolov8-baseline\baseline-yolov8n-640-e50-b8-v2\weights\best.pt`
- Dataset split: test
- Test images: 457
- Test instances: 1636
- Prediction output: `D:\science-data\runs\fruits-yolov8-baseline\baseline-yolov8n-640-e50-b8-v2-predict-test`
- Test validation output: `D:\science-data\runs\fruits-yolov8-baseline\baseline-yolov8n-640-e50-b8-v2-val-test`

## Test Metrics

| Class | Images | Instances | Precision | Recall | mAP50 | mAP50-95 |
|---|---:|---:|---:|---:|---:|---:|
| all | 457 | 1636 | 0.527 | 0.415 | 0.408 | 0.269 |
| Apple | 113 | 422 | 0.576 | 0.341 | 0.419 | 0.299 |
| Banana | 88 | 174 | 0.548 | 0.460 | 0.420 | 0.254 |
| Grape | 94 | 366 | 0.592 | 0.440 | 0.433 | 0.269 |
| Orange | 92 | 511 | 0.545 | 0.321 | 0.349 | 0.209 |
| Pineapple | 40 | 87 | 0.422 | 0.333 | 0.325 | 0.195 |
| Watermelon | 47 | 76 | 0.480 | 0.592 | 0.499 | 0.389 |

Precision means how often predicted boxes are correct. Recall means how many real objects are found. mAP50 is a looser detection score. mAP50-95 is stricter because boxes must match the object more accurately.

## Visual Samples

| Sample | Ground Truth | Prediction | Main Observation |
|---|---|---|---|
| Batch 0 | `figures/test-batch0-labels.jpg` | `figures/test-batch0-pred.jpg` | Large fruits are often detected, but grouped fruit annotations and single-fruit predictions do not always match. |
| Batch 1 | `figures/test-batch1-labels.jpg` | `figures/test-batch1-pred.jpg` | Some non-fruit areas are predicted as fruit, and grape/pineapple confusion appears. |
| Batch 2 | `figures/test-batch2-labels.jpg` | `figures/test-batch2-pred.jpg` | The model works on obvious large targets, but struggles with cluttered market scenes and inconsistent annotation style. |

## Main Error Types

1. Low recall on dense or cluttered scenes

The model misses many objects when there are many fruits in one image. This is visible in dense apple, orange, and grape scenes. The test recall is only 0.415, so missed detections are a major problem.

2. Inconsistent box style

Some labels use one large box for a whole fruit group, while other labels use many boxes for individual fruits. The model sometimes predicts several small boxes where the label expects one large box, or predicts one large box where the label expects individual boxes. This hurts mAP even when the visual prediction looks reasonable.

3. False positives on fruit-like objects

The model sometimes detects non-fruit regions as fruit, such as hooks, background objects, or printed/painted fruit-like areas. False positives lower precision.

4. Class confusion

Pineapple and grape sometimes get confused in visually unusual scenes. Orange and apple also become harder when the image is crowded, partly because both can be round and similarly colored under some lighting.

5. Weak classes on test set

Pineapple has the weakest mAP50-95 at 0.195. Orange also has low recall at 0.321. Watermelon has the best mAP50-95 at 0.389, probably because watermelon examples are visually more distinctive.

## Likely Causes

- The dataset is visually diverse: real fruit photos, market scenes, product photos, and even paintings or printed fruit-like objects appear.
- Some classes have fewer examples, especially Pineapple and Watermelon.
- Labeling style is not fully consistent between group-level boxes and instance-level boxes.
- YOLOv8n is a small model, so it has limited capacity for cluttered scenes and unusual images.
- The baseline used default training settings, with no class-specific tuning or data cleaning.

## Next Experiments

1. Run YOLOv8s

YOLOv8s is larger than YOLOv8n. It may improve recall and reduce missed detections, but training will be slower.

2. Lower confidence threshold during prediction

The current prediction used `conf=0.25`. Lowering it to `0.15` may find more objects, but it can also add more false positives.

3. Clean or subset the dataset

Create a cleaner agricultural subset with real fruit photos only. This may better match the agricultural detection direction.

4. Inspect class distribution and hard samples

Count each class and collect hard examples for Orange, Pineapple, and dense fruit scenes.

5. Try image size 960

Larger image size may help small or dense targets, but it costs more GPU memory and training time.
