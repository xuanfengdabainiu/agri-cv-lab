# Metrics

| Run | Date | Model | Dataset Split | Epochs | Image Size | Precision | Recall | mAP50 | mAP50-95 | Counting RMSE | Blue Percentage RMSE | Notes |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| yolov8l-1920-e50-b1-local-seed42 | 2026-06-29 | YOLOv8l | local seed42 val | 50 | 1920 | 0.86003 | 0.77750 | 0.86768 | 0.56141 | - | - | best epoch 48 |
| yolov8l-1920-e20-b1-local-seed42 | 2026-06-29 | YOLOv8l | local seed42 val | 20 | 1920 | 0.77062 | 0.68240 | 0.75591 | 0.46523 | - | - | best epoch 19; training manually stopped after epoch 20 |
| reproduce-yolov8l-2560 | planned | YOLOv8l | official | - | 2560 | - | - | - | - | - | - | paper main setting |
| reproduce-yolov9c-2560 | planned | YOLOv9-c | official | - | 2560 | - | - | - | - | - | - | paper main setting |
| reproduce-yolov8l-3520 | planned | YOLOv8l | official | - | 3520 | - | - | - | - | - | - | highest-resolution setting if hardware allows |
