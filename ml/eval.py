"""Evaluation gate that refuses to emit accuracy without a real model and dataset."""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from ml.dataset import read_metadata, summary
from tools.provenance import generated_provenance


def write_status(path: pathlib.Path, status: str, reason: str, config: dict, metadata: dict | None = None) -> None:
    payload = {"provenance": generated_provenance(config), "status": status, "label": "NOT_A_RESULT", "reason": reason}
    if metadata is not None:
        payload["metadata_check"] = metadata
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate inputs for VaaniCore leave-one-speaker-out evaluation")
    parser.add_argument("--metadata", help="recording metadata CSV")
    parser.add_argument("--model", help="trained model path")
    parser.add_argument("--output", default="results/ml_eval_status.json")
    args = parser.parse_args()
    config = {"metadata": args.metadata, "model": args.model}
    output = ROOT / args.output
    if not args.metadata:
        write_status(output, "BLOCKED_INPUT", "labelled metadata CSV is required", config)
        print(output)
        return 2
    try:
        rows = read_metadata(args.metadata)
    except (OSError, ValueError) as exc:
        write_status(output, "BLOCKED_DATASET", str(exc), config)
        print(output)
        return 2
    metadata = summary(rows)
    if len(metadata["speakers"]) < 3:
        write_status(output, "BLOCKED_DATASET", "at least three speakers are required", config, metadata)
        print(output)
        return 2
    if not args.model:
        write_status(output, "BLOCKED_MODEL", "trained model and representative evaluation configuration are required", config, metadata)
        print(output)
        return 2
    model_path = ROOT / args.model
    if not model_path.exists():
        write_status(output, "BLOCKED_MODEL", "trained model path does not exist", config, metadata)
        print(output)
        return 2
    try:
        import tensorflow  # noqa: F401
    except ImportError:
        write_status(output, "BLOCKED_TOOLCHAIN", "TensorFlow is not installed", config, metadata)
        print(output)
        return 2
    # Full evaluation is intentionally kept behind the real toolchain and
    # model-data path; no score is emitted by this gate itself.
    write_status(output, "BLOCKED_EVALUATION", "model evaluation implementation requires the pinned training artifact and LOSO run configuration", config, metadata)
    print(output)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
