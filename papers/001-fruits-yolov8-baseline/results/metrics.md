# Metrics

| Run | Date | Model | Dataset Split | Epochs | Image Size | Precision | Recall | mAP50 | mAP50-95 | Notes |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| baseline-001 | planned | YOLOv8n | val | 50 | 640 | - | - | - | - | initial baseline |
| smoke-yolov8n-320 | 2026-06-07 | YOLOv8n | val | 1 | 320 | 0.29064 | 0.28016 | 0.18047 | 0.10253 | smoke test only |
| baseline-yolov8n-640-e50-b8-v2 | 2026-06-07 | YOLOv8n | val | 50 | 640 | 0.638 | 0.441 | 0.478 | 0.320 | validated with best.pt |
| baseline-yolov8n-640-e50-b8-v2 | 2026-06-21 | YOLOv8n | test | 50 | 640 | 0.527 | 0.415 | 0.408 | 0.269 | best.pt on held-out test split |
| compare-yolov8s-640-e20-b8 | 2026-06-22 | YOLOv8s | val | 20 | 640 | 0.592 | 0.450 | 0.481 | 0.310 | quick compare; stopped at epoch 20 |
| compare-yolov8s-640-e20-b8 | 2026-06-22 | YOLOv8s | test | 20 | 640 | 0.515 | 0.408 | 0.414 | 0.266 | best.pt on held-out test split |
