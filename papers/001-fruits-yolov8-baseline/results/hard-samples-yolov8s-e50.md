# YOLOv8s 50-Epoch Hard Samples

## Purpose

This note analyzes hard test samples for the YOLOv8s 50-epoch model. The goal is to check whether longer training reduces the errors seen in the YOLOv8s 20-epoch run.

## Model Files

Original pretrained model file:

- YOLOv8s pretrained file: `C:\Users\liuqilu\Documents\science\agri-cv-lab\yolov8s.pt`

Trained model file:

- YOLOv8s 50-epoch best weights: `D:\science-data\runs\fruits-yolov8-baseline\compare-yolov8s-640-e50-b8-v2\weights\best.pt`

## Run

- Model: YOLOv8s
- Epochs: 50
- Dataset split: test
- Test validation output: `D:\science-data\runs\fruits-yolov8-baseline\compare-yolov8s-640-e50-b8-v2-val-test`

## Test Metrics

| Model | Epochs | Precision | Recall | mAP50 | mAP50-95 |
|---|---:|---:|---:|---:|---:|
| YOLOv8n | 50 | 0.527 | 0.415 | 0.408 | 0.269 |
| YOLOv8s | 20 | 0.515 | 0.408 | 0.414 | 0.266 |
| YOLOv8s | 50 | 0.542 | 0.438 | 0.439 | 0.294 |

YOLOv8s 50 epochs improves all four test metrics compared with YOLOv8n 50 epochs and YOLOv8s 20 epochs. The improvement is useful but still moderate.

## Visual Samples

| Sample | Ground Truth | Prediction | Main Problem |
|---|---|---|---|
| Batch 0 | `figures/yolov8s-e50-batch0-labels.jpg` | `figures/yolov8s-e50-batch0-pred.jpg` | More conservative boxes, but still affected by dense fruit groups and decorative objects. |
| Batch 1 | `figures/yolov8s-e50-batch1-labels.jpg` | `figures/yolov8s-e50-batch1-pred.jpg` | Better confidence on common fruits, but decorative or unusual objects still cause mistakes. |
| Batch 2 | `figures/yolov8s-e50-batch2-labels.jpg` | `figures/yolov8s-e50-batch2-pred.jpg` | Market scenes, paintings, and cluttered backgrounds remain difficult. |

## Observed Error Types

### 1. Conservative Group Boxes

Compared with the 20-epoch YOLOv8s run, the 50-epoch model often predicts fewer boxes in dense scenes. For example, it may use one larger box for a group of bananas, apples, or oranges.

This can reduce false positives, but it may also miss individual fruits when the label expects one box per fruit.

### 2. Dense Fruit and Label-Style Mismatch

The dataset still mixes group boxes and individual boxes. This makes dense fruit scenes difficult to evaluate.

Example:

- A bowl or basket may contain many fruits, but the label may use one large box or only a few boxes.
- The model may make a visually reasonable prediction but still lose metric score if its box style differs from the label style.

### 3. False Positives on Decorative or Printed Objects

The model still detects fruit-like objects that are not clean real-fruit detection targets.

Examples:

- printed apple-like shapes
- grape-shaped decorations
- fruit in paintings or decorative scenes
- market signs or background objects shaped like fruit

This still affects Precision.

### 4. Missed Objects in Cluttered Scenes

The model still misses small, occluded, far-away, or cluttered fruits. This is visible in market scenes, background fruit groups, and dense natural scenes.

This still affects Recall.

### 5. Class Confusion

Some unusual objects or cropped fruit appearances still produce wrong class predictions. This is especially visible for pineapple, grape, apple, orange, and banana in non-standard scenes.

## Comparison With YOLOv8s 20 Epochs

The 50-epoch model is generally better than the 20-epoch model on test metrics:

- Precision improves from 0.515 to 0.542.
- Recall improves from 0.408 to 0.438.
- mAP50 improves from 0.414 to 0.439.
- mAP50-95 improves from 0.266 to 0.294.

Visually, the 50-epoch model appears more conservative and cleaner in some images. It often produces fewer low-confidence boxes than the 20-epoch model.

However, the main hard cases are not fully solved. The same dataset issues still appear:

- mixed image styles
- group-box vs instance-box inconsistency
- decorative or printed fruit-like objects
- cluttered scenes and small objects

## Current Conclusion

Training YOLOv8s for 50 epochs makes the comparison fairer and improves the test metrics. YOLOv8s 50 epochs is better than YOLOv8n 50 epochs on this test split.

But the improvement is moderate, and hard samples show that data quality is still a major bottleneck. The next useful direction is to build a cleaner subset or clean the labels before trying more model changes.

## Next Step Ideas

1. Update the YOLOv8n-vs-YOLOv8s comparison document with the 50-epoch YOLOv8s result.
2. Create a cleaner real-fruit subset and remove paintings, printed images, and decorative objects.
3. Compare the original dataset against the cleaner subset.
4. If continuing model experiments, try data cleaning before larger model changes.
