# Application Metrics

Date: 2026-06-29

Run: `yolov8l-1920-e50-b1-local-seed42`

Evaluation split: local seed42 test

Method:

- Count ground-truth boxes from YOLO test labels.
- Count predicted boxes from YOLO prediction labels at confidence `0.25`.
- Counting error is `predicted total - ground-truth total` per image.
- Blue percentage is `Blue count / total count * 100` per image.
- RMSE is computed across the 14 test images.

Important note:

- This follows the count-from-detections application setting.
- It does not perform one-to-one IoU matching for the application metrics.
- Detection quality is already evaluated separately by mAP.

## Summary

| Metric | Value | Unit |
|---|---:|---|
| Counting RMSE | 6.9334 | berries/image |
| Blue Percentage RMSE | 7.8007 | percentage points |

## Per-Image Values

| Image | True Total | Pred Total | Count Error | True Blue % | Pred Blue % | Blue % Error |
|---|---:|---:|---:|---:|---:|---:|
| MSState_YL_Cropped_0007 | 77 | 70 | -7 | 14.29 | 14.29 | +0.00 |
| MSState_YL_Cropped_0008 | 49 | 44 | -5 | 38.78 | 43.18 | +4.41 |
| MSState_YL_Cropped_0009 | 120 | 108 | -12 | 30.00 | 28.70 | -1.30 |
| MSState_YL_Cropped_0024 | 58 | 54 | -4 | 20.69 | 29.63 | +8.94 |
| MSState_YL_Cropped_0025 | 173 | 176 | +3 | 31.79 | 34.09 | +2.30 |
| MSState_YL_Cropped_0028 | 55 | 40 | -15 | 9.09 | 7.50 | -1.59 |
| MSState_YL_Cropped_0030 | 112 | 112 | +0 | 13.39 | 13.39 | +0.00 |
| MSState_YL_Cropped_0031 | 88 | 80 | -8 | 25.00 | 26.25 | +1.25 |
| MSState_YL_Cropped_0037 | 26 | 25 | -1 | 26.92 | 52.00 | +25.08 |
| MSState_YL_Cropped_0057 | 108 | 100 | -8 | 12.04 | 22.00 | +9.96 |
| MSState_YL_Cropped_0059 | 181 | 182 | +1 | 15.47 | 17.58 | +2.11 |
| MSState_YL_Cropped_0064 | 53 | 48 | -5 | 28.30 | 31.25 | +2.95 |
| MSState_YL_Cropped_0072 | 169 | 168 | -1 | 34.91 | 34.52 | -0.39 |
| MSState_YL_Cropped_0110 | 94 | 87 | -7 | 10.64 | 10.34 | -0.29 |

## Interpretation

- Lower Counting RMSE means the model's fruit count is closer to the ground truth.
- Lower Blue Percentage RMSE means the model's maturity-ratio estimate is closer to the ground truth.
- The current errors are computed on only 14 test images, so they should be treated as first reproduction results rather than final paper-level claims.
