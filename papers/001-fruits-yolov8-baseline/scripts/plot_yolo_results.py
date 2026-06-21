from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


RUN_DIR = Path(r"D:\science-data\runs\fruits-yolov8-baseline\baseline-yolov8n-640-e50-b8-v2")
OUTPUT_DIR = Path(r"C:\Users\liuqilu\Documents\science\agri-cv-lab\papers\001-fruits-yolov8-baseline\results\figures")


def main():
    results_csv = RUN_DIR / "results.csv"
    if not results_csv.exists():
        raise FileNotFoundError(f"Cannot find results.csv: {results_csv}")

    df = pd.read_csv(results_csv)
    df.columns = [column.strip() for column in df.columns]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    plot_metrics(df, OUTPUT_DIR / "baseline-yolov8n-map-curve.png")
    plot_losses(df, OUTPUT_DIR / "baseline-yolov8n-loss-curve.png")

    print(f"Saved figures to: {OUTPUT_DIR}")


def plot_metrics(df, output_path):
    plt.figure(figsize=(8, 5))
    plt.plot(df["epoch"], df["metrics/mAP50(B)"], label="mAP50", linewidth=2)
    plt.plot(df["epoch"], df["metrics/mAP50-95(B)"], label="mAP50-95", linewidth=2)
    plt.plot(df["epoch"], df["metrics/precision(B)"], label="Precision", linewidth=1.5, alpha=0.8)
    plt.plot(df["epoch"], df["metrics/recall(B)"], label="Recall", linewidth=1.5, alpha=0.8)
    plt.xlabel("Epoch")
    plt.ylabel("Score")
    plt.title("YOLOv8n Validation Metrics")
    plt.grid(True, linestyle="--", alpha=0.35)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def plot_losses(df, output_path):
    plt.figure(figsize=(8, 5))
    plt.plot(df["epoch"], df["train/box_loss"], label="train box loss", linewidth=2)
    plt.plot(df["epoch"], df["train/cls_loss"], label="train cls loss", linewidth=2)
    plt.plot(df["epoch"], df["train/dfl_loss"], label="train dfl loss", linewidth=2)
    plt.plot(df["epoch"], df["val/box_loss"], label="val box loss", linewidth=1.5, linestyle="--")
    plt.plot(df["epoch"], df["val/cls_loss"], label="val cls loss", linewidth=1.5, linestyle="--")
    plt.plot(df["epoch"], df["val/dfl_loss"], label="val dfl loss", linewidth=1.5, linestyle="--")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title("YOLOv8n Training and Validation Loss")
    plt.grid(True, linestyle="--", alpha=0.35)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


if __name__ == "__main__":
    main()
