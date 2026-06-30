# Experiment Summary

Date: 2026-06-30

Project:

- Canopy Image-based Blueberry Detection by YOLOv8 and YOLOv9

Current reproduction stage:

- First-stage local reproduction completed.
- This is a local, hardware-aware reproduction, not an exact reproduction of the paper's highest-resolution setting.
- The project can now be paused as a completed first-stage reproduction and used as a reference for the next paper.

## What Was Done

Completed steps:

- Downloaded and verified the BlueberryDCM dataset.
- Cloned and inspected the official code.
- Set up the `blueberry-yolo` Conda environment.
- Inspected label formats and class IDs.
- Created a fixed local train/val/test split with seed `42`.
- Remapped the YOLO labels from class IDs `0` and `3` to standard two-class IDs:
  - `0`: Unblue
  - `1`: Blue
- Trained YOLOv8l at image size 1920 for 20 epochs.
- Trained YOLOv8l at image size 1920 for 50 epochs.
- Attempted YOLOv8l at image size 2560, but stopped before epoch 1 because of GPU memory pressure.
- Evaluated the 50-epoch model on the local test split.
- Generated prediction images for the test split.
- Wrote the first error analysis.
- Computed Counting RMSE and Blue Percentage RMSE.
- Downloaded the official YOLOv9-c pretrained weight.
- Patched local YOLOv9 code for PyTorch 2.6+ checkpoint loading.
- Ran a YOLOv9-c 640 smoke test successfully.
- Attempted a YOLOv9-c 1920 smoke test and confirmed that it exceeds the local GPU memory limit.

## Data Split

The official split folders referenced by the code were not included in the released Zenodo dataset.

Therefore, this project uses a fixed local split:

| Split | Images |
|---|---:|
| train | 112 |
| val | 14 |
| test | 14 |

The split is saved in:

- `configs/split-local-seed42/`

## Main Result

Best completed run:

- `yolov8l-1920-e50-b1-local-seed42`

Validation result:

| Eval Split | Best Epoch | Precision | Recall | mAP50 | mAP50-95 |
|---|---:|---:|---:|---:|---:|
| val | 48 | 0.86003 | 0.77750 | 0.86768 | 0.56141 |

Test result:

| Eval Split | Precision | Recall | mAP50 | mAP50-95 | Counting RMSE | Blue Percentage RMSE |
|---|---:|---:|---:|---:|---:|---:|
| test | 0.88500 | 0.83100 | 0.89700 | 0.60500 | 6.9334 | 7.8007 |

The test result is strong for a first local reproduction, but the test set only has 14 images, so it should be interpreted carefully.

## 20 Epochs vs 50 Epochs

Longer training improved the validation result clearly.

| Run | Eval Split | mAP50 | mAP50-95 |
|---|---|---:|---:|
| YOLOv8l 1920 e20 | val | 0.75591 | 0.46523 |
| YOLOv8l 1920 e50 | val | 0.86768 | 0.56141 |

Conclusion:

- 20 epochs was not enough.
- 50 epochs produced a much better model.

## Difference From The Paper

This experiment is not an exact reproduction of the paper's best setting.

Main differences:

- The official train/val/test split was not available in the released dataset.
- The paper reports high-resolution settings such as 2560 and 3520.
- This local run used 1920 because 2560 was too memory-heavy on the laptop GPU.
- The paper reports results from the authors' original split and hardware setup.
- This project reports results from the local seed42 split.

Hardware limitation:

- The attempted 2560 run used almost all available 8 GB GPU memory and did not complete epoch 1 in a practical amount of time.
- YOLOv9-c at image size 1920 failed during the first epoch with CUDA out-of-memory.
- YOLOv9-c at image size 1920 reported about 12.4 GB GPU memory demand, while the laptop GPU has about 8 GB.

## YOLOv9-c Feasibility Check

YOLOv9-c was tested only as a feasibility check, not as a formal result.

Successful smoke test:

| Run | Split | Epochs | Image Size | Batch | Precision | Recall | mAP50 | mAP50-95 | Notes |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| smoke-yolov9c-640-e1-b1-local-seed42-final | val | 1 | 640 | 1 | 0.335 | 0.485 | 0.361 | 0.209 | environment check only |

Failed 1920 attempt:

| Run | Epochs | Image Size | Batch | Result | Reason |
|---|---:|---:|---:|---|---|
| smoke-yolov9c-1920-e1-b1-local-seed42 | 1 | 1920 | 1 | failed | CUDA out-of-memory |

Conclusion:

- The local environment can run YOLOv9-c.
- YOLOv9-c at 640 is technically runnable but too small to represent the paper setting.
- YOLOv9-c at 1920 is not feasible on the current laptop GPU.
- A formal YOLOv9-c reproduction should be done on a larger GPU or with memory-saving changes.

## Error Analysis

Main observed patterns:

- The model tends to under-count Unblue berries.
- The model slightly over-predicts Blue berries.
- Dense images remain more difficult.
- Some images are counted very accurately, such as `MSState_YL_Cropped_0030` and `MSState_YL_Cropped_0072`.

Count-level summary on the test split:

| Class | Ground Truth | Predicted | Difference |
|---|---:|---:|---:|
| Unblue | 1,056 | 970 | -86 |
| Blue | 307 | 324 | +17 |
| Total | 1,363 | 1,294 | -69 |

This suggests the model misses some unripe berries and sometimes shifts ambiguous berries toward the Blue class.

## Current Files To Know

Important local artifacts:

- Dataset: `D:\science-data\datasets\blueberry-dcm`
- Best weights: `D:\science-data\runs\blueberry-yolov8-yolov9-reproduction\yolov8l-1920-e50-b1-local-seed42\weights\best.pt`
- Test predictions: `D:\science-data\runs\blueberry-yolov8-yolov9-reproduction\yolov8l-1920-e50-b1-local-seed42-test-predict`
- YOLOv9-c pretrained weight: `D:\science-data\weights\yolov9\yolov9-c.pt`
- YOLOv9-c 640 smoke test: `D:\science-data\runs\blueberry-yolov8-yolov9-reproduction\smoke-yolov9c-640-e1-b1-local-seed42-final`
- YOLOv9-c 1920 failed attempt: `D:\science-data\runs\blueberry-yolov8-yolov9-reproduction\smoke-yolov9c-1920-e1-b1-local-seed42`

Important Git-tracked files:

- `results/metrics.md`
- `results/error-analysis.md`
- `results/application-metrics.md`
- `results/experiment-summary.md`
- `scripts/prepare_local_split.py`
- `scripts/compute_application_metrics.py`
- `configs/blueberry-local-seed42.yaml`
- `configs/split-local-seed42/`

## Stage Conclusion

This paper's first-stage reproduction can be paused here.

What was achieved:

- A usable local YOLOv8l reproduction was completed.
- The local test split was evaluated.
- Paper-related application metrics were computed.
- Error patterns were summarized.
- The local hardware limit for YOLOv9-c 1920 was tested and documented.

Why it should be paused:

- The missing official split prevents exact comparison with the paper.
- The current laptop GPU prevents high-resolution YOLOv9-c reproduction.
- Continuing this paper locally would mostly become hardware tuning rather than useful learning.

Recommended handoff:

- Use this project as the standard workflow template for future paper reproductions.
- Start the next paper with the same structure:
  - paper notes
  - dataset inspection
  - environment record
  - baseline run
  - metrics table
  - reproduction log
  - error analysis
  - experiment summary

Optional future work for this paper:

- Run YOLOv9-c on a larger GPU.
- Try lower YOLOv9-c image sizes such as 1280 or 1536.
- Compare YOLOv8s, YOLOv8m, and YOLOv8l at image size 1920.
- Improve counting and Blue percentage estimation using post-processing.
