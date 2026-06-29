from __future__ import annotations

import math
from collections import Counter
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
TRUE_LABEL_DIR = Path(r"D:\science-data\datasets\blueberry-dcm\yolo-local-split\labels\test")
PRED_LABEL_DIR = Path(
    r"D:\science-data\runs\blueberry-yolov8-yolov9-reproduction"
    r"\yolov8l-1920-e50-b1-local-seed42-test-predict\labels"
)
OUTPUT_MD = PROJECT_DIR / "results" / "application-metrics.md"

RUN_NAME = "yolov8l-1920-e50-b1-local-seed42"
CONFIDENCE = 0.25


def count_labels(path: Path) -> Counter[int]:
    counts: Counter[int] = Counter()
    if not path.exists():
        return counts
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        class_id = int(float(raw.split()[0]))
        counts[class_id] += 1
    return counts


def rmse(errors: list[float]) -> float:
    if not errors:
        raise ValueError("Cannot compute RMSE from an empty list.")
    return math.sqrt(sum(error * error for error in errors) / len(errors))


def blue_percentage(blue_count: int, total_count: int) -> float:
    if total_count == 0:
        return 0.0
    return blue_count / total_count * 100


def format_float(value: float) -> str:
    return f"{value:.4f}"


def main() -> None:
    true_files = sorted(TRUE_LABEL_DIR.glob("*.txt"))
    if not true_files:
        raise RuntimeError(f"No ground-truth labels found in {TRUE_LABEL_DIR}")

    rows = []
    count_errors: list[float] = []
    blue_pct_errors: list[float] = []

    for true_file in true_files:
        pred_file = PRED_LABEL_DIR / true_file.name
        true_counts = count_labels(true_file)
        pred_counts = count_labels(pred_file)

        true_unblue = true_counts[0]
        true_blue = true_counts[1]
        pred_unblue = pred_counts[0]
        pred_blue = pred_counts[1]

        true_total = true_unblue + true_blue
        pred_total = pred_unblue + pred_blue
        count_error = pred_total - true_total

        true_blue_pct = blue_percentage(true_blue, true_total)
        pred_blue_pct = blue_percentage(pred_blue, pred_total)
        blue_pct_error = pred_blue_pct - true_blue_pct

        count_errors.append(count_error)
        blue_pct_errors.append(blue_pct_error)

        rows.append(
            {
                "image": true_file.stem,
                "true_total": true_total,
                "pred_total": pred_total,
                "count_error": count_error,
                "true_blue_pct": true_blue_pct,
                "pred_blue_pct": pred_blue_pct,
                "blue_pct_error": blue_pct_error,
            }
        )

    counting_rmse = rmse(count_errors)
    blue_pct_rmse = rmse(blue_pct_errors)

    lines = [
        "# Application Metrics",
        "",
        "Date: 2026-06-29",
        "",
        f"Run: `{RUN_NAME}`",
        "",
        "Evaluation split: local seed42 test",
        "",
        "Method:",
        "",
        "- Count ground-truth boxes from YOLO test labels.",
        f"- Count predicted boxes from YOLO prediction labels at confidence `{CONFIDENCE}`.",
        "- Counting error is `predicted total - ground-truth total` per image.",
        "- Blue percentage is `Blue count / total count * 100` per image.",
        "- RMSE is computed across the 14 test images.",
        "",
        "Important note:",
        "",
        "- This follows the count-from-detections application setting.",
        "- It does not perform one-to-one IoU matching for the application metrics.",
        "- Detection quality is already evaluated separately by mAP.",
        "",
        "## Summary",
        "",
        "| Metric | Value | Unit |",
        "|---|---:|---|",
        f"| Counting RMSE | {format_float(counting_rmse)} | berries/image |",
        f"| Blue Percentage RMSE | {format_float(blue_pct_rmse)} | percentage points |",
        "",
        "## Per-Image Values",
        "",
        "| Image | True Total | Pred Total | Count Error | True Blue % | Pred Blue % | Blue % Error |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]

    for row in rows:
        lines.append(
            "| {image} | {true_total} | {pred_total} | {count_error:+d} | {true_blue_pct:.2f} | {pred_blue_pct:.2f} | {blue_pct_error:+.2f} |".format(
                **row
            )
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Lower Counting RMSE means the model's fruit count is closer to the ground truth.",
            "- Lower Blue Percentage RMSE means the model's maturity-ratio estimate is closer to the ground truth.",
            "- The current errors are computed on only 14 test images, so they should be treated as first reproduction results rather than final paper-level claims.",
            "",
        ]
    )

    OUTPUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"run={RUN_NAME}")
    print(f"images={len(rows)}")
    print(f"counting_rmse={format_float(counting_rmse)}")
    print(f"blue_percentage_rmse={format_float(blue_pct_rmse)}")
    print(f"output={OUTPUT_MD}")


if __name__ == "__main__":
    main()
