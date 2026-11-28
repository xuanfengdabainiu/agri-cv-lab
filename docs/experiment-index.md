# Experiment Index

| ID | Name | Type | Dataset | Code Source | Status | Best Result |
|---|---|---|---|---|---|---|
| 000 | Template | template | - | - | template | - |
| 001 | Fruits YOLOv8 Baseline | baseline | lightly-ai/dataset_fruits_detection | Ultralytics YOLOv8 | done | YOLOv8s 50e test mAP50 0.439 |
| 002 | Blueberry YOLOv8/YOLOv9 Reproduction | reproduction | BlueberryDCM | vicdxxx/BlueberryDetectionAndCounting | setup | full reproduction planned |
| 003 | CitDet Citrus Detection | reproduction | - | - | planned | local folder scaffold only, not yet in Git |
| 004 | Blueberry bZIP Genome-Wide Reproduction | reproduction | Draper V1.0 genome; public RNA-seq BioProjects | Feng et al. (2025) methods | done | 102 VcbZIP genes and both stress-response lists reproduced at table level; MEME and PlantCARE stages blocked on Linux tooling |
| 005 | Blueberry Fruit-Trait Genomic Prediction | reproduction | USDA-ARS PNW blueberry SNP and fruit/ripening phenotypes | Hislop et al. code; rrBLUP | reproducing | Core quality, fruit mass, height, and bloom50 done; split leakage audited across seven traits |

## Status Values

- `planned`: not started
- `setup`: environment or dataset preparation
- `baseline`: baseline training is running or complete
- `reproducing`: reproducing paper method
- `improving`: adding my own changes
- `done`: completed and summarized
- `paused`: blocked or intentionally stopped
