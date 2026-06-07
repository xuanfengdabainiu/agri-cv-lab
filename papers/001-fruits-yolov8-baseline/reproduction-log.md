# Reproduction Log

## 2026-06-07

Goal:

- Create the experiment folder and define the first YOLOv8 baseline plan.

Environment:

- OS: Windows
- Python: TBD
- CUDA: TBD
- PyTorch: TBD
- Key packages: ultralytics, torch

Command:

```bash
# Planned
conda env create -f envs/yolo-env.yml
conda activate agri-yolo
yolo detect train data=papers/001-fruits-yolov8-baseline/configs/data.yaml model=yolov8n.pt epochs=50 imgsz=640
```

Config Changes:

- Created standard experiment structure.
- Dataset path is not configured yet.
- Created local storage paths:
  - `D:\science-data\datasets\fruits-detection`
  - `D:\science-data\runs\fruits-yolov8-baseline`
  - `D:\science-data\weights`

Results:

- Precision:
- Recall:
- mAP50:
- mAP50-95:

Problems:

- Dataset has not been downloaded yet.
- Need to confirm GPU/CUDA before installing PyTorch.

Fixes:

- TBD

Next Step:

- Check GPU/CUDA.
- Download dataset outside Git.
- Create `configs/data.yaml`.
- Install YOLO environment.
