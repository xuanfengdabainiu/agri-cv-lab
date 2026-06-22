# Experiment Summary

## Purpose

This experiment is the first baseline practice for agricultural object detection. The main goal is not to propose a new method yet, but to learn a complete YOLO workflow:

- prepare a dataset
- configure the environment
- train a baseline model
- validate and test the trained weights
- inspect prediction errors
- compare a slightly larger model
- keep reproducible experiment records

The task is fruit detection with six classes: Apple, Banana, Grape, Orange, Pineapple, and Watermelon.

## Experiments

### Experiment 1: YOLOv8n Baseline

- Model: YOLOv8n
- Epochs: 50
- Image size: 640
- Batch size: 8
- Main run: `baseline-yolov8n-640-e50-b8-v2`
- Best weights: `D:\science-data\runs\fruits-yolov8-baseline\baseline-yolov8n-640-e50-b8-v2\weights\best.pt`

YOLOv8n is the smallest model in the YOLOv8 family. It is fast and suitable as the first baseline.

### Experiment 2: YOLOv8s Quick Compare

- Model: YOLOv8s
- Epochs: 20
- Image size: 640
- Batch size: 8
- Main run: `compare-yolov8s-640-e20-b8`
- Best weights: `D:\science-data\runs\fruits-yolov8-baseline\compare-yolov8s-640-e20-b8\weights\best.pt`

YOLOv8s is larger than YOLOv8n. It has more parameters and may have better learning ability, but it trains more slowly. This run was originally started with 50 epochs, then stopped at epoch 20 to save time.

## Results

### Validation Set

The validation set is used during training to check model performance and select `best.pt`.

| Model | Epochs | Precision | Recall | mAP50 | mAP50-95 |
|---|---:|---:|---:|---:|---:|
| YOLOv8n | 50 | 0.638 | 0.441 | 0.478 | 0.320 |
| YOLOv8s | 20 | 0.592 | 0.450 | 0.481 | 0.310 |

On the validation set, YOLOv8s has slightly higher Recall and mAP50, but lower Precision and mAP50-95. This means YOLOv8s may find a few more objects, but its predictions are not clearly more accurate overall.

### Test Set

The test set is used after training to check final generalization.

| Model | Epochs | Precision | Recall | mAP50 | mAP50-95 |
|---|---:|---:|---:|---:|---:|
| YOLOv8n | 50 | 0.527 | 0.415 | 0.408 | 0.269 |
| YOLOv8s | 20 | 0.515 | 0.408 | 0.414 | 0.266 |

On the test set, YOLOv8s only slightly improves mAP50, while Precision, Recall, and mAP50-95 are slightly lower. The difference is small, so YOLOv8s 20 epochs cannot be considered clearly better than YOLOv8n 50 epochs.

## What The Metrics Mean

- Precision: among the boxes predicted by the model, how many are correct. Higher Precision means fewer false detections.
- Recall: among the real objects, how many are found by the model. Higher Recall means fewer missed objects.
- mAP50: a common detection score using a looser box-matching standard.
- mAP50-95: a stricter detection score. It requires boxes to be more accurately located, so it is usually lower than mAP50.

## Main Findings

1. YOLOv8n is a usable baseline

YOLOv8n completed the full 50-epoch training and produced a working `best.pt`. It gives a reasonable first baseline, but the test Recall is only 0.415, so missed detections are still common.

2. YOLOv8s has potential but is not clearly better yet

YOLOv8s reached similar performance after only 20 epochs, which suggests that a larger model may be useful. However, the test results do not show a clear improvement. A fairer comparison would require training YOLOv8s for 50 epochs.

3. Validation results and test results are different

Both models perform better on the validation set than on the test set. This means the test set is harder or less similar to the training data. The test set result is more important when judging final generalization.

4. Recall is still a key problem

Both models have relatively low Recall. This means the models still miss many real fruits, especially in dense or cluttered scenes.

5. Dataset quality affects the result

The dataset contains many different image types, including real fruit photos, market scenes, product photos, and some unusual images. The annotation style is also not fully consistent: some images use one large box for a group of fruits, while others use many boxes for individual fruits. This makes training and evaluation harder.

## Current Conclusion

The first baseline workflow has been completed successfully. YOLOv8n 50 epochs is the current main baseline. YOLOv8s 20 epochs is a useful quick comparison, but it is not enough to prove that YOLOv8s is better.

At this stage, the most important result is not only the model score, but also that the full experiment process has been established:

- data is stored on D drive
- code and records are stored in GitHub
- metrics are recorded in `metrics.md`
- errors are analyzed in `error-analysis.md`
- training curves can be plotted with Python

## Next Steps

1. Continue YOLOv8s to 50 epochs

This would make the comparison with YOLOv8n fairer, but it will take more time.

2. Analyze hard examples

Collect images where the model misses objects or predicts wrong classes. This can help identify whether the main problem is small objects, dense scenes, class confusion, or noisy labels.

3. Try a lower confidence threshold

Lowering the prediction confidence threshold may improve Recall, but it may also reduce Precision by adding more false detections.

4. Practice Python analysis

Continue using Python to read `results.csv`, plot curves, compare runs, and summarize metrics automatically.

5. Consider a cleaner agricultural dataset

The current dataset is useful for learning YOLO, but it is visually mixed. A cleaner fruit or crop dataset may be better for future agricultural detection experiments.
