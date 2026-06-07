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

## 2026-06-07 Smoke Test

Goal:

- Verify that YOLOv8 can read the dataset, use the GPU, train for one epoch, and write outputs to the D drive run folder.

Command:

```bash
yolo detect train data=papers/001-fruits-yolov8-baseline/configs/data.yaml model=yolov8n.pt epochs=1 imgsz=320 batch=8 device=0 project=D:/science-data/runs/fruits-yolov8-baseline name=smoke-yolov8n-320 exist_ok=True workers=4
```

Run Output:

- Run folder: `D:\science-data\runs\fruits-yolov8-baseline\smoke-yolov8n-320`
- Time: 63.78 seconds
- Model: YOLOv8n
- Epochs: 1
- Image size: 320
- Batch: 8
- Device: CUDA GPU

Results:

- Precision: 0.29064
- Recall: 0.28016
- mAP50: 0.18047
- mAP50-95: 0.10253

Problems:

- Running through `conda run` caused a Windows GBK encoding error after training output was produced.
- The training itself completed and generated validation plots/results.
- The `weights` folder was created but no weight file was present after this smoke run.

Fixes:

- For future runs, call `D:\conda_envs\agri-yolo\Scripts\yolo.exe` directly instead of using `conda run`.

Next Step:

- Run a real baseline with YOLOv8n, `epochs=50`, `imgsz=640`, and a reasonable batch size.

## 2026-06-07 Baseline Training

Goal:

- Train the first full YOLOv8n baseline for 50 epochs at image size 640.

Command:

```bash
yolo detect train data=papers/001-fruits-yolov8-baseline/configs/data.yaml model=yolov8n.pt epochs=50 imgsz=640 batch=8 device=0 project=D:/science-data/runs/fruits-yolov8-baseline name=baseline-yolov8n-640-e50-b8-v2 workers=4
```

Run Output:

- Run folder: `D:\science-data\runs\fruits-yolov8-baseline\baseline-yolov8n-640-e50-b8-v2`
- Best weights: `D:\science-data\runs\fruits-yolov8-baseline\baseline-yolov8n-640-e50-b8-v2\weights\best.pt`
- Last weights: `D:\science-data\runs\fruits-yolov8-baseline\baseline-yolov8n-640-e50-b8-v2\weights\last.pt`
- Model: YOLOv8n
- Epochs: 50
- Image size: 640
- Batch: 8
- Device: CUDA GPU

Validation Command:

```bash
yolo detect val data=papers/001-fruits-yolov8-baseline/configs/data.yaml model=D:/science-data/runs/fruits-yolov8-baseline/baseline-yolov8n-640-e50-b8-v2/weights/best.pt imgsz=640 batch=8 device=0 project=D:/science-data/runs/fruits-yolov8-baseline name=baseline-yolov8n-640-e50-b8-v2-val-best workers=4
```

Results:

- Precision: 0.638
- Recall: 0.441
- mAP50: 0.478
- mAP50-95: 0.320

Per-class mAP50:

- Apple: 0.500
- Banana: 0.484
- Grape: 0.382
- Orange: 0.405
- Pineapple: 0.513
- Watermelon: 0.586

Problems:

- The first baseline attempt failed after epoch 1 when `polars==1.41.2` raised `RuntimeError: unknown feature flag: 'sse3'` while Ultralytics was saving/reading `results.csv`.

Fixes:

- Reinstalled `polars==1.33.1`.
- Reran the baseline with a new run name, `baseline-yolov8n-640-e50-b8-v2`.

Next Step:

- Inspect predictions visually.
- Try a stronger baseline such as YOLOv8s or tune data augmentation.
