from __future__ import annotations

import random
import shutil
from pathlib import Path


SEED = 42

SOURCE_DIR = Path(r"D:\science-data\datasets\blueberry-dcm\extracted\Dataset")
OUTPUT_DIR = Path(r"D:\science-data\datasets\blueberry-dcm\yolo-local-split")
PROJECT_DIR = Path(__file__).resolve().parents[1]
SPLIT_DIR = PROJECT_DIR / "configs" / "split-local-seed42"
DATA_YAML = PROJECT_DIR / "configs" / "blueberry-local-seed42.yaml"

CLASS_NAMES = {
    0: "Unblue",
    1: "Blue",
}


def reset_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def remap_yolo_label(src: Path, dst: Path) -> int:
    count = 0
    lines = []
    for raw in src.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        parts = raw.split()
        class_id = int(float(parts[0]))
        if class_id == 3:
            class_id = 1
        elif class_id != 0:
            raise ValueError(f"Unexpected class id {class_id} in {src}")
        lines.append(" ".join([str(class_id), *parts[1:]]))
        count += 1
    dst.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return count


def write_split_list(name: str, stems: list[str]) -> None:
    path = SPLIT_DIR / f"{name}.txt"
    path.write_text("\n".join(stems) + "\n", encoding="utf-8")


def main() -> None:
    images = sorted(SOURCE_DIR.glob("*.jpg"))
    if len(images) != 140:
        raise RuntimeError(f"Expected 140 images, found {len(images)}")

    stems = [image.stem for image in images]
    rng = random.Random(SEED)
    rng.shuffle(stems)

    train = sorted(stems[:112])
    val = sorted(stems[112:126])
    test = sorted(stems[126:])
    splits = {"train": train, "val": val, "test": test}

    reset_dir(OUTPUT_DIR)
    for split in splits:
        (OUTPUT_DIR / "images" / split).mkdir(parents=True, exist_ok=True)
        (OUTPUT_DIR / "labels" / split).mkdir(parents=True, exist_ok=True)

    SPLIT_DIR.mkdir(parents=True, exist_ok=True)

    total_boxes = 0
    for split, split_stems in splits.items():
        write_split_list(split, split_stems)
        for stem in split_stems:
            shutil.copy2(SOURCE_DIR / f"{stem}.jpg", OUTPUT_DIR / "images" / split / f"{stem}.jpg")
            total_boxes += remap_yolo_label(
                SOURCE_DIR / f"{stem}.txt",
                OUTPUT_DIR / "labels" / split / f"{stem}.txt",
            )

    DATA_YAML.write_text(
        "\n".join(
            [
                f"path: {OUTPUT_DIR.as_posix()}",
                "train: images/train",
                "val: images/val",
                "test: images/test",
                "names:",
                f"  0: {CLASS_NAMES[0]}",
                f"  1: {CLASS_NAMES[1]}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(f"seed={SEED}")
    print(f"source={SOURCE_DIR}")
    print(f"output={OUTPUT_DIR}")
    print(f"train={len(train)} val={len(val)} test={len(test)}")
    print(f"boxes={total_boxes}")
    print(f"data_yaml={DATA_YAML}")
    print(f"split_dir={SPLIT_DIR}")


if __name__ == "__main__":
    main()
