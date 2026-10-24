"""Train the VaaniCore command model when real labelled audio is available."""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
import wave

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from ml.dataset import read_metadata
from ml.features import mfcc
from ml.model import build_model
from tools.provenance import generated_provenance


def _status(path: pathlib.Path, status: str, reason: str, config: dict) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"provenance": generated_provenance(config), "status": status,
                                "label": "NOT_A_RESULT", "reason": reason}, indent=2) + "\n")
    print(path)
    return 2


def _read_audio(path: pathlib.Path) -> np.ndarray:
    with wave.open(str(path), "rb") as stream:
        if stream.getnchannels() != 1 or stream.getsampwidth() != 2 or stream.getframerate() != 16_000:
            raise ValueError(f"{path}: expected mono 16-bit 16 kHz WAV")
        return np.frombuffer(stream.readframes(stream.getnframes()), dtype="<i2").astype(np.float32) / 32768.0


def main() -> int:
    parser = argparse.ArgumentParser(description="Train the 14-class int8-ready VaaniCore command model")
    parser.add_argument("--metadata", required=True)
    parser.add_argument("--output", default="models/command.keras")
    parser.add_argument("--status", default="results/ml_train_status.json")
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--batch-size", type=int, default=32)
    args = parser.parse_args()
    config = {"metadata": args.metadata, "output": args.output, "epochs": args.epochs, "batch_size": args.batch_size}
    status = pathlib.Path(args.status)
    try:
        import tensorflow as tf  # noqa: F401
    except ImportError:
        return _status(status, "BLOCKED_TOOLCHAIN", "TensorFlow is not installed", config)
    try:
        rows = read_metadata(args.metadata)
    except (OSError, ValueError) as exc:
        return _status(status, "BLOCKED_DATASET", str(exc), config)
    if len({row["speaker_id"] for row in rows}) < 3:
        return _status(status, "BLOCKED_DATASET", "at least three speakers are required", config)
    classes = json.loads((ROOT / "ml/configs/classes.json").read_text())["classes"]
    class_to_id = {name: index for index, name in enumerate(classes)}
    features, labels = [], []
    try:
        for row in rows:
            if row["label"] not in class_to_id:
                raise ValueError(f"unknown label: {row['label']}")
            values = mfcc(_read_audio(ROOT / row["path"]))
            padded = np.zeros((124, 10), dtype=np.float32)
            padded[:min(124, len(values))] = values[:124]
            features.append(padded[..., None])
            labels.append(class_to_id[row["label"]])
    except (OSError, ValueError, wave.Error) as exc:
        return _status(status, "BLOCKED_DATASET", str(exc), config)
    model = build_model(len(classes))
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    model.fit(np.asarray(features), np.asarray(labels), epochs=args.epochs, batch_size=args.batch_size, verbose=2)
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    model.save(output)
    status.write_text(json.dumps({"provenance": generated_provenance(config), "status": "TRAINED",
        "label": "TRAINING_ARTIFACT — NOT AN EVALUATION RESULT", "clips": len(rows),
        "speakers": len({r['speaker_id'] for r in rows}), "model": str(output)}, indent=2) + "\n")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
