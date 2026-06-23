# Dataset Inspection

Date: 2026-06-23

Dataset:

- Name: BlueberryDCM
- Source: https://zenodo.org/records/14002517
- Local archive: `D:\science-data\datasets\blueberry-dcm\BlueberryDCM.7z`
- Local extracted folder: `D:\science-data\datasets\blueberry-dcm\extracted\Dataset`

## File Integrity

The downloaded archive was verified before extraction.

| Item | Value |
|---|---|
| Official size | `107267412` bytes |
| Local size | `107267412` bytes |
| Official MD5 | `77fc808520dbe7751cb367dbd06ea32f` |
| Local MD5 | `77fc808520dbe7751cb367dbd06ea32f` |
| Result | passed |

## Extracted Files

| Extension | Count | Meaning |
|---|---:|---|
| `.jpg` | 140 | RGB blueberry canopy images |
| `.txt` | 140 | YOLO-format annotations |
| `.xml` | 140 | Pascal VOC-style annotations |
| `.json` | 140 | VIA-style annotations |

The dataset is stored as one flat folder. It does not include ready-made `images/train`, `images/val`, or `images/test` folders.

## Image Names

There are two filename groups:

| Prefix | Count |
|---|---:|
| `MSState_YL` | 134 |
| `MSU_Josh` | 6 |

The `MSState_YL_Cropped_0016` image is not present, so the filename sequence has one missing index. This is not an error by itself because the dataset still contains 140 complete image-label groups.

## YOLO TXT Labels

The `.txt` labels are valid YOLO-format lines:

```text
class_id x_center y_center width height
```

All coordinates are normalized between 0 and 1.

Label check:

| Item | Value |
|---|---:|
| TXT files | 140 |
| Total boxes | 17955 |
| Bad YOLO lines | 0 |

Class counts from `.txt`:

| Class ID | Count |
|---:|---:|
| 0 | 10981 |
| 3 | 6974 |

Important note:

- The TXT labels only use class IDs `0` and `3`.
- This means the released YOLO labels already merge visibility sub-classes into two maturity classes:
  - `0`: Unblue
  - `3`: Blue

## XML Labels

The `.xml` labels preserve four detailed classes:

| XML class | Count |
|---|---:|
| `Unblue_visible` | 4142 |
| `Unblue_occluded` | 6839 |
| `Blue_visible` | 1722 |
| `Blue_occluded` | 5252 |

Total XML boxes: 17955

The XML counts explain the TXT merge:

| Detailed XML classes | Merged TXT class |
|---|---:|
| `Unblue_visible` + `Unblue_occluded` | 0 |
| `Blue_visible` + `Blue_occluded` | 3 |

This matches the official YOLOv8 config idea in `yolov8/config.py`:

```text
merge_labels_dict = {2: 0, 1: 3}
immature_label_idx = 0
mature_label_idx = 3
```

## Official Code Expectations

The official YOLOv8 config files reference these folders:

```text
train2017.0
val2017.0
test2017.0
```

The official YOLOv9 config also references:

```text
train2017.0
test2017.0
```

These split folders are not included in the downloaded Zenodo archive.

This means the public dataset is complete as raw images and annotations, but the exact train/validation/test split used by the authors is not directly present.

## Reproduction Risk

Main issue:

- Exact paper reproduction is blocked unless the official split can be recovered.

Why this matters:

- If we create our own split, the experiment is still valid and reproducible, but the metrics may not exactly match the paper.
- Small datasets are sensitive to split changes. With only 140 images, moving a few difficult images between train and test can noticeably change mAP, counting RMSE, and Blue percentage RMSE.

## Recommended Next Step

Create a documented local split from the released dataset, then train on that split.

Recommended local split:

- `train`: 112 images
- `val`: 14 images
- `test`: 14 images

Rules:

- Use a fixed random seed.
- Copy or symlink images and TXT labels into YOLO-compatible folders.
- Remap class `3` to class `1` for standard two-class YOLO training unless using the official four-class index convention.
- Save the exact split list in Git so future runs use the same images.

Suggested class names after remapping:

```text
0: Unblue
1: Blue
```

If we want to stay closer to the author's index convention, we can keep class IDs `0` and `3`, but many YOLO tools expect class IDs to be continuous from `0` to `nc - 1`. Therefore remapping `3 -> 1` is safer for local reproduction.
