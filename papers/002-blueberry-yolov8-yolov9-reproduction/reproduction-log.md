# Reproduction Log

## 2026-06-23 Project Setup

Goal:

- Create a new reproduction project for **Canopy Image-based Blueberry Detection by YOLOv8 and YOLOv9**.
- Follow the same project structure used by the first Fruits YOLOv8 baseline experiment.

Sources:

- Paper: https://ssrn.com/abstract=4981340
- Code: https://github.com/vicdxxx/BlueberryDetectionAndCounting
- Dataset: https://zenodo.org/records/14002517

What was created:

- `README.md`
- `paper-notes.md`
- `reproduction-log.md`
- `configs/`
- `scripts/`
- `results/`
- `results/metrics.md`
- `results/figures/`

Initial plan:

- Download the BlueberryDCM dataset to `D:\science-data\datasets\blueberry-dcm`.
- Download or inspect the official GitHub code.
- Identify the exact dataset split, label format, training parameters, and evaluation scripts.
- Reproduce YOLOv8l experiments.
- Reproduce YOLOv9-c experiments.
- Compute detection mAP, counting RMSE, and Blue fruit percentage RMSE.

Notes:

- This project is planned as a full reproduction of the paper's main experiments.
- Large files must stay on D drive and should not be committed to Git.

## 2026-06-23 Plan Updated to Full Reproduction

Reason:

- The project should target full paper reproduction, not a simplified beginner baseline.

Updated plan:

- Reproduce YOLOv8l and YOLOv9-c experiments from the paper.
- Use the paper's high-resolution settings such as 2560 and 3520 image size when hardware allows.
- Record any hardware-driven changes, such as smaller batch size.
- Compute both detection metrics and application metrics:
  - mAP
  - fruit counting RMSE
  - Blue fruit percentage RMSE

Immediate next step:

- Download the BlueberryDCM dataset and official code to D drive.
- Inspect the official file structure before writing configs or commands.

## 2026-06-23 Environment Setup

Goal:

- Prepare a separate environment for the Blueberry YOLOv8/YOLOv9 full reproduction.
- Keep it separate from the previous Fruits YOLOv8 experiment environment.

Local code:

- Official repository: `D:\science-data\code\BlueberryDetectionAndCounting`
- GitHub URL: https://github.com/vicdxxx/BlueberryDetectionAndCounting
- Checked commit: `c47858d`

Environment:

- Conda environment: `D:\conda_envs\blueberry-yolo`
- Python: 3.10.20
- PyTorch: 2.11.0+cu128
- TorchVision: 0.26.0+cu128
- CUDA available: yes
- GPU: NVIDIA GeForce RTX 5060 Laptop GPU
- Ultralytics: 8.4.61

Important packages:

- `opencv-python==4.13.0.92`
- `Pillow==9.5.0`
- `pandas==2.3.3`
- `albumentations==2.0.8`
- `pycocotools==2.0.11`
- `tensorboard==2.20.0`
- `polars==1.33.1`

Validation:

- YOLOv8 CLI works with `D:\conda_envs\blueberry-yolo\Scripts\yolo.exe`.
- YOLOv9 `train.py --help` loads successfully.
- YOLOv8 official `train_yolov8.py` currently fails because `config_da.py` is missing from the repository.

Notes:

- The official YOLOv8 script also contains author-specific Windows paths. For exact reproduction, this must be inspected and adapted carefully.
- YOLOv9 appears more directly runnable once the dataset YAML and weights are prepared.
- Environment record added: `configs/environment.yaml`.

## 2026-06-23 Dataset Download and Extraction

Goal:

- Download and verify the public BlueberryDCM dataset from Zenodo.
- Keep the dataset on D drive, not in the Git repository.

Dataset source:

- Zenodo record: https://zenodo.org/records/14002517
- File: `BlueberryDCM.7z`
- Official file size: `107267412` bytes
- Official MD5: `77fc808520dbe7751cb367dbd06ea32f`

Local dataset:

- Archive: `D:\science-data\datasets\blueberry-dcm\BlueberryDCM.7z`
- Extracted folder: `D:\science-data\datasets\blueberry-dcm\extracted\Dataset`

Download notes:

- Single-connection download from Zenodo was very slow and failed twice before completion.
- The final download was completed by splitting the file into byte ranges, downloading ranges in parallel, and merging them.
- Final local file size: `107267412` bytes
- Final local MD5: `77fc808520dbe7751cb367dbd06ea32f`
- Conclusion: the downloaded archive matches the official Zenodo checksum.

Extracted file count:

- `.jpg`: 140
- `.json`: 140
- `.txt`: 140
- `.xml`: 140

Notes:

- Each image appears to have three annotation formats: JSON, TXT, and XML.
- Next step is dataset inspection: confirm label format, class IDs, split strategy, and whether the official code expects YOLO TXT, VOC XML, or JSON annotations.

## 2026-06-23 Dataset Inspection

Goal:

- Inspect the extracted dataset before writing training configs.
- Confirm annotation format, class IDs, and whether an official train/val/test split is available.

Inspection report:

- `results/dataset-inspection.md`

Findings:

- The extracted dataset contains 140 images.
- Each image has `.txt`, `.xml`, and `.json` annotations.
- The `.txt` annotations are valid YOLO-format labels.
- The YOLO labels contain 17,955 total boxes.
- The YOLO labels only use class IDs `0` and `3`:
  - `0`: Unblue
  - `3`: Blue
- The XML labels preserve four detailed classes:
  - `Unblue_visible`: 4,142
  - `Unblue_occluded`: 6,839
  - `Blue_visible`: 1,722
  - `Blue_occluded`: 5,252

Important reproduction issue:

- The released Zenodo archive does not include the official `train2017.0`, `val2017.0`, or `test2017.0` split folders referenced by the official code.
- This means exact paper reproduction is blocked unless the official split can be recovered.

Next step:

- Create a documented local train/val/test split from the released 140 images.
- Save the split lists in Git.
- Remap YOLO class `3` to `1` for a standard two-class setup:
  - `0`: Unblue
  - `1`: Blue

## 2026-06-23 Local Train/Val/Test Split

Goal:

- Create a simple fixed split for the first reproduction.
- Use the released data even though the official split folders are missing.

Script:

- `scripts/prepare_local_split.py`

Inputs:

- Source folder: `D:\science-data\datasets\blueberry-dcm\extracted\Dataset`
- Source labels: original YOLO `.txt` labels with class IDs `0` and `3`

Outputs:

- YOLO dataset folder: `D:\science-data\datasets\blueberry-dcm\yolo-local-split`
- YOLO data config: `configs/blueberry-local-seed42.yaml`
- Split lists:
  - `configs/split-local-seed42/train.txt`
  - `configs/split-local-seed42/val.txt`
  - `configs/split-local-seed42/test.txt`

Split settings:

- Random seed: `42`
- Train: 112 images
- Val: 14 images
- Test: 14 images

Label handling:

- Original class `0` kept as `0`: Unblue
- Original class `3` remapped to `1`: Blue
- Final class counts:
  - `0`: 10,981 boxes
  - `1`: 6,974 boxes
- Total boxes after conversion: 17,955

Reason:

- This is the first reproduction, so the split is intentionally simple.
- The split is still fixed and documented, so future runs can reproduce the same data setup.

Validation check:

- Command used:

```text
D:\conda_envs\blueberry-yolo\Scripts\yolo.exe detect val data=C:\Users\liuqilu\Documents\science\agri-cv-lab\papers\002-blueberry-yolov8-yolov9-reproduction\configs\blueberry-local-seed42.yaml model=yolov8n.pt imgsz=640 batch=4 device=0 project=D:\science-data\runs\blueberry-yolov8-yolov9-reproduction name=data-check-yolov8n-640
```

- Result: YOLO successfully read the local validation split.
- Val images: 14
- Val boxes: 959
- Saved run folder: `D:\science-data\runs\blueberry-yolov8-yolov9-reproduction\data-check-yolov8n-640`

Note:

- This was only a data loading check, not a real model evaluation.
- The command used COCO-pretrained `yolov8n.pt`, so the printed class names came from COCO and the metrics were zero.
- This is expected and does not indicate a dataset problem.

## 2026-06-29 YOLOv8l 1920 Training

Goal:

- Start the first real YOLOv8l reproduction run on the local seed42 split.
- Use image size 1920 as a middle step before trying the paper's higher-resolution settings.

Command:

```text
D:\conda_envs\blueberry-yolo\Scripts\yolo.exe detect train data=C:\Users\liuqilu\Documents\science\agri-cv-lab\papers\002-blueberry-yolov8-yolov9-reproduction\configs\blueberry-local-seed42.yaml model=yolov8l.pt epochs=100 imgsz=1920 batch=1 device=0 project=D:\science-data\runs\blueberry-yolov8-yolov9-reproduction name=yolov8l-1920-e100-b1-local-seed42 workers=4 patience=100 close_mosaic=50 seed=42
```

Actual run:

- User requested stopping at epoch 20.
- Training was manually stopped after epoch 20.
- Run folder: `D:\science-data\runs\blueberry-yolov8-yolov9-reproduction\yolov8l-1920-e20-b1-local-seed42`
- Weights:
  - `weights\best.pt`
  - `weights\last.pt`

Settings:

- Model: YOLOv8l
- Dataset split: local seed42
- Image size: 1920
- Batch size: 1
- Completed epochs: 20
- Device: RTX 5060 Laptop GPU

Best validation result:

- Best epoch: 19
- Precision: 0.77062
- Recall: 0.68240
- mAP50: 0.75591
- mAP50-95: 0.46523

Last epoch result:

- Epoch: 20
- Precision: 0.83011
- Recall: 0.64287
- mAP50: 0.75025
- mAP50-95: 0.45129

Notes:

- The run was originally launched with `epochs=100`, but was stopped at epoch 20 by request.
- The local run folder was renamed from `yolov8l-1920-e100-b1-local-seed42` to `yolov8l-1920-e20-b1-local-seed42` so the folder name matches the actual completed epoch count.
- `best.pt` is expected to correspond to epoch 19 because epoch 19 had the best validation mAP.
- Counting RMSE and Blue percentage RMSE were not computed yet.

## 2026-06-29 YOLOv8l 2560 Attempt Stopped

Goal:

- Try a 20-epoch YOLOv8l run at image size 2560 to move closer to the paper's main high-resolution setting.
- Report progress every 5 epochs if the run was able to progress normally.

Command:

```text
D:\conda_envs\blueberry-yolo\Scripts\yolo.exe detect train data=C:\Users\liuqilu\Documents\science\agri-cv-lab\papers\002-blueberry-yolov8-yolov9-reproduction\configs\blueberry-local-seed42.yaml model=yolov8l.pt epochs=20 imgsz=2560 batch=1 device=0 project=D:\science-data\runs\blueberry-yolov8-yolov9-reproduction name=yolov8l-2560-e20-b1-local-seed42 workers=0 patience=20 close_mosaic=10 seed=42
```

Outcome:

- The run was manually stopped before completing epoch 1.
- No `results.csv` was produced.
- No validation metrics were available.
- No `best.pt` or `last.pt` was produced.

Local folder:

- `D:\science-data\runs\blueberry-yolov8-yolov9-reproduction\yolov8l-2560-e20-b1-local-seed42`

Files left by the interrupted run:

- `args.yaml`
- `labels.jpg`
- `train_batch0.jpg`
- `train_batch1.jpg`
- `train_batch2.jpg`
- empty `weights\` folder

Reason:

- The run used almost all available GPU memory.
- Observed GPU memory while running: about 7.75 GB used out of 8 GB.
- The machine had only about 50-60 MB free GPU memory during the attempt.
- Training did not finish the first epoch after a long wait, so the run was stopped by request.

Decision:

- Do not treat this as a valid metrics run.
- Keep it in the reproduction log as a resource-limited attempt.
- Next practical option is to use 1920 for longer training, or try an intermediate image size such as 2240 before returning to 2560.

## 2026-06-29 YOLOv8l 1920 50-Epoch Training

Goal:

- Extend the successful 1920 YOLOv8l setup from 20 epochs to 50 epochs.
- Compare whether longer training improves validation performance on the local seed42 split.

Command:

```text
D:\conda_envs\blueberry-yolo\Scripts\yolo.exe detect train data=C:\Users\liuqilu\Documents\science\agri-cv-lab\papers\002-blueberry-yolov8-yolov9-reproduction\configs\blueberry-local-seed42.yaml model=yolov8l.pt epochs=50 imgsz=1920 batch=1 device=0 project=D:\science-data\runs\blueberry-yolov8-yolov9-reproduction name=yolov8l-1920-e50-b1-local-seed42 workers=4 patience=50 close_mosaic=25 seed=42
```

Run folder:

- `D:\science-data\runs\blueberry-yolov8-yolov9-reproduction\yolov8l-1920-e50-b1-local-seed42`

Settings:

- Model: YOLOv8l
- Dataset split: local seed42
- Image size: 1920
- Batch size: 1
- Epochs: 50
- Device: RTX 5060 Laptop GPU

Best validation result:

- Best epoch: 48
- Precision: 0.86003
- Recall: 0.77750
- mAP50: 0.86768
- mAP50-95: 0.56141

Final epoch result:

- Epoch: 50
- Precision: 0.85239
- Recall: 0.77773
- mAP50: 0.85786
- mAP50-95: 0.55221

Weights:

- `weights\best.pt`
- `weights\last.pt`

Hardware notes:

- GPU was heavily used during training.
- Checked GPU temperature near the end of training: about 71-76 C, which was acceptable for this laptop run.

Comparison with 20-epoch run:

- 20-epoch best mAP50-95: 0.46523
- 50-epoch best mAP50-95: 0.56141
- Longer training clearly improved validation performance.

Remaining work:

- Run test-set evaluation with `best.pt`.
- Compute counting RMSE and Blue percentage RMSE.
