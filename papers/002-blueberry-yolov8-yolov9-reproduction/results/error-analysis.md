# Error Analysis

Date: 2026-06-29

Run:

- `yolov8l-1920-e50-b1-local-seed42`

Model:

- `D:\science-data\runs\blueberry-yolov8-yolov9-reproduction\yolov8l-1920-e50-b1-local-seed42\weights\best.pt`

Prediction folder:

- `D:\science-data\runs\blueberry-yolov8-yolov9-reproduction\yolov8l-1920-e50-b1-local-seed42-test-predict`

Copied example figures:

- `results/figures/test-predictions/`

## Test Result Summary

The model was evaluated on the local seed42 test split before this error analysis.

| Split | Images | Boxes | Precision | Recall | mAP50 | mAP50-95 |
|---|---:|---:|---:|---:|---:|---:|
| test | 14 | 1,363 | 0.885 | 0.831 | 0.897 | 0.605 |

Per-class result:

| Class | Instances | Precision | Recall | mAP50 | mAP50-95 |
|---|---:|---:|---:|---:|---:|
| Unblue | 1,056 | 0.926 | 0.820 | 0.902 | 0.623 |
| Blue | 307 | 0.843 | 0.842 | 0.891 | 0.586 |

## Count-Level Inspection

This inspection compares the number of ground-truth boxes and predicted boxes per image.
It is not a replacement for mAP because it does not check IoU matching, but it is useful for spotting likely under-counting or over-counting images.

| Image | True Unblue | True Blue | Pred Unblue | Pred Blue | Total Difference |
|---|---:|---:|---:|---:|---:|
| `MSState_YL_Cropped_0007` | 66 | 11 | 60 | 10 | -7 |
| `MSState_YL_Cropped_0008` | 30 | 19 | 25 | 19 | -5 |
| `MSState_YL_Cropped_0009` | 84 | 36 | 77 | 31 | -12 |
| `MSState_YL_Cropped_0024` | 46 | 12 | 38 | 16 | -4 |
| `MSState_YL_Cropped_0025` | 118 | 55 | 116 | 60 | +3 |
| `MSState_YL_Cropped_0028` | 50 | 5 | 37 | 3 | -15 |
| `MSState_YL_Cropped_0030` | 97 | 15 | 97 | 15 | 0 |
| `MSState_YL_Cropped_0031` | 66 | 22 | 59 | 21 | -8 |
| `MSState_YL_Cropped_0037` | 19 | 7 | 12 | 13 | -1 |
| `MSState_YL_Cropped_0057` | 95 | 13 | 78 | 22 | -8 |
| `MSState_YL_Cropped_0059` | 153 | 28 | 150 | 32 | +1 |
| `MSState_YL_Cropped_0064` | 38 | 15 | 33 | 15 | -5 |
| `MSState_YL_Cropped_0072` | 110 | 59 | 110 | 58 | -1 |
| `MSState_YL_Cropped_0110` | 84 | 10 | 78 | 9 | -7 |

Total count comparison:

| Class | Ground Truth | Predicted | Difference |
|---|---:|---:|---:|
| Unblue | 1,056 | 970 | -86 |
| Blue | 307 | 324 | +17 |
| Total | 1,363 | 1,294 | -69 |

## Main Error Patterns

1. The model tends to under-count `Unblue`.

The test split has 1,056 Unblue boxes, but the prediction output at confidence 0.25 contains 970 Unblue boxes.
This suggests missed detections are more common for unripe berries.

2. The model slightly over-predicts `Blue`.

The test split has 307 Blue boxes, while predictions contain 324 Blue boxes.
This may indicate some Unblue berries are being classified as Blue, especially in visually ambiguous or shaded areas.

3. Dense scenes are still difficult.

Images with many berries show larger count gaps.
Examples:

- `MSState_YL_Cropped_0028`: total difference -15
- `MSState_YL_Cropped_0009`: total difference -12
- `MSState_YL_Cropped_0057`: total difference -8

4. Some images are handled very well.

Examples:

- `MSState_YL_Cropped_0030`: exact total count match, 97 Unblue and 15 Blue in both ground truth and predictions.
- `MSState_YL_Cropped_0072`: total difference -1.

## Representative Figures

The following prediction images were copied into the repository for quick review:

| Image | Reason |
|---|---|
| `MSState_YL_Cropped_0030.jpg` | Count-level match is very good. |
| `MSState_YL_Cropped_0072.jpg` | Large dense image with near-matching total count. |
| `MSState_YL_Cropped_0028.jpg` | Clear under-counting case. |
| `MSState_YL_Cropped_0057.jpg` | Unblue under-counting and Blue over-prediction. |
| `MSState_YL_Cropped_0037.jpg` | Blue over-prediction relative to ground truth. |

## Limitations of This Analysis

- The count comparison uses raw prediction counts at confidence 0.25.
- It does not perform one-to-one IoU matching with ground-truth boxes.
- Counting RMSE and Blue percentage RMSE are reported separately in `results/application-metrics.md`.
- The local seed42 test split has only 14 images, so image-level conclusions should be treated cautiously.

## Next Step

Use this analysis to choose the next experiment, such as a smaller YOLOv8 model comparison or an intermediate image size.
