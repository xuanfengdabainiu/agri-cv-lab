#!/usr/bin/env python3
"""Check whether experiment commits follow docs/workflow.md."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
LARGE_FILE_LIMIT = 25 * 1024 * 1024
LARGE_FILE_EXTENSIONS = {
    ".7z",
    ".ckpt",
    ".onnx",
    ".pth",
    ".pt",
    ".rar",
    ".tar",
    ".zip",
}


def run_git(args: list[str]) -> str:
    return subprocess.check_output(["git", *args], cwd=REPO, text=True, stderr=subprocess.STDOUT)


def normalize(path: str) -> str:
    return path.replace("\\", "/")


def diff_name_status(base: str, head: str) -> list[tuple[str, str]]:
    raw = run_git(["diff", "--name-status", base, head])
    changes: list[tuple[str, str]] = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        status = parts[0]
        path = parts[-1]
        changes.append((status, normalize(path)))
    return changes


def find_base_head(argv: list[str]) -> tuple[str, str]:
    if len(argv) >= 3:
        base, head = argv[1], argv[2]
    else:
        base = os.environ.get("BASE_SHA", "")
        head = os.environ.get("HEAD_SHA", "HEAD")

    if not base or set(base) == {"0"}:
        try:
            base = run_git(["rev-parse", f"{head}^"]).strip()
        except subprocess.CalledProcessError:
            base = run_git(["hash-object", "-t", "tree", "/dev/null"]).strip()

    return base, head


def experiment_of(path: str) -> str | None:
    parts = path.split("/")
    if len(parts) >= 2 and parts[0] == "papers":
        return "/".join(parts[:2])
    return None


def is_meaningful_experiment_change(path: str) -> bool:
    if path.endswith("/.gitkeep"):
        return False
    parts = path.split("/")
    if len(parts) < 3 or parts[0] != "papers":
        return False
    return parts[2] in {"configs", "results", "scripts"}


def check_reproduction_logs(changes: list[tuple[str, str]]) -> list[str]:
    touched_experiments: set[str] = set()
    updated_logs: set[str] = set()

    for _status, path in changes:
        exp = experiment_of(path)
        if not exp:
            continue
        if path == f"{exp}/reproduction-log.md":
            updated_logs.add(exp)
        if is_meaningful_experiment_change(path):
            touched_experiments.add(exp)

    errors = []
    for exp in sorted(touched_experiments - updated_logs):
        errors.append(
            f"{exp}: configs/results/scripts changed, but {exp}/reproduction-log.md was not updated."
        )
    return errors


def check_new_experiment_structure(changes: list[tuple[str, str]]) -> list[str]:
    experiments = sorted(
        {
            exp
            for status, path in changes
            if status.startswith("A") and (exp := experiment_of(path))
        }
    )

    errors = []
    required = ["README.md", "paper-notes.md", "reproduction-log.md", "results/metrics.md"]
    for exp in experiments:
        missing = [name for name in required if not (REPO / exp / name).exists()]
        if missing:
            errors.append(f"{exp}: new experiment is missing required files: {', '.join(missing)}.")
    return errors


def check_large_files(changes: list[tuple[str, str]]) -> list[str]:
    errors = []
    for status, path in changes:
        if status.startswith("D"):
            continue
        full_path = REPO / path
        if not full_path.exists() or not full_path.is_file():
            continue

        suffix = full_path.suffix.lower()
        size = full_path.stat().st_size
        if suffix in LARGE_FILE_EXTENSIONS:
            errors.append(f"{path}: large artifact extension '{suffix}' should not be committed.")
        elif size > LARGE_FILE_LIMIT:
            mb = size / 1024 / 1024
            errors.append(f"{path}: file is {mb:.1f} MB; large artifacts should stay under D:/science-data.")
    return errors


def main(argv: list[str]) -> int:
    base, head = find_base_head(argv)
    changes = diff_name_status(base, head)

    errors = []
    errors.extend(check_reproduction_logs(changes))
    errors.extend(check_new_experiment_structure(changes))
    errors.extend(check_large_files(changes))

    if errors:
        print("Workflow check failed:\n")
        for error in errors:
            print(f"- {error}")
        print("\nSee docs/workflow.md for the repository workflow.")
        return 1

    print("Workflow check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
