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
