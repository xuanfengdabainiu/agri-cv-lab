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

## 2026-06-07 Dataset Download

Goal:

- Download the public fruit detection dataset and verify the YOLO directory structure.

Dataset:

- Source: https://github.com/lightly-ai/dataset_fruits_detection
- Local path: `D:\science-data\datasets\fruits-detection`
- Images: 8479 `.jpg`
- Labels: 8479 `.txt`
- Classes: Apple, Banana, Grape, Orange, Pineapple, Watermelon

Command:

```bash
git clone https://github.com/lightly-ai/dataset_fruits_detection.git D:\science-data\datasets\fruits-detection
```

Config Changes:

- Added `configs/data.yaml` pointing to the D drive dataset path.

Problems:

- None so far.

Next Step:

- Create and test the `agri-yolo` conda environment.

## 2026-06-07 Environment Setup

Goal:

- Create the `agri-yolo` conda environment and verify YOLOv8 with GPU acceleration.

Environment:

- Conda env: `agri-yolo`
- Location: `D:\conda_envs\agri-yolo`
- Python: 3.10.20
- Ultralytics: 8.4.61
- PyTorch: 2.11.0+cu128
- CUDA: 12.8
- GPU: NVIDIA GeForce RTX 5060 Laptop GPU, 8151 MiB

Commands:

```bash
conda env create -f envs/yolo-env.yml
conda run -n agri-yolo python -m pip install --upgrade --force-reinstall torch torchvision --index-url https://download.pytorch.org/whl/cu128
conda run -n agri-yolo yolo checks
```

Results:

- `torch.cuda.is_available()` returned `True`.
- `yolo checks` detected CUDA GPU successfully.

Problems:

- Initial environment installed CPU-only PyTorch.

Fixes:

- Reinstalled `torch` and `torchvision` from the PyTorch CUDA 12.8 wheel index.
- Updated `envs/yolo-env.yml` to include the CUDA wheel index.

Next Step:

- Run a small YOLOv8 smoke test on the fruit dataset.
