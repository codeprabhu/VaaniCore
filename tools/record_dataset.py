"""Record one labelled command set from a human microphone."""
from __future__ import annotations

import argparse
import csv
import json
import pathlib
import sys
import wave

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from tools.provenance import generated_provenance

SAMPLE_RATE = 16_000
CLASSES = {
    "open_amplifier", "open_filter", "open_regulator", "open_last", "open_yesterday",
    "run_sim", "open_amp_run_sim", "open_yday_run_sim", "show_result", "cancel",
    "confirm", "close_project", "_unknown_", "_silence_",
}
FIELDS = ["path", "label", "speaker_id", "distance_m", "room", "sample_rate", "clipped", "trim_start", "trim_end"]


def _trim(samples: np.ndarray, threshold: float = 0.015, padding: int = 800) -> tuple[np.ndarray, int, int]:
    normalized = np.abs(samples.astype(np.float32)) / 32768.0
    active = np.flatnonzero(normalized > threshold)
    if active.size == 0:
        return samples, 0, len(samples)
    start = max(0, int(active[0]) - padding)
    end = min(len(samples), int(active[-1]) + padding + 1)
    return samples[start:end], start, end


def _write_wav(path: pathlib.Path, samples: np.ndarray) -> None:
    with wave.open(str(path), "wb") as stream:
        stream.setnchannels(1)
        stream.setsampwidth(2)
        stream.setframerate(SAMPLE_RATE)
        stream.writeframes(np.asarray(samples, dtype=np.int16).tobytes())


def main() -> int:
    parser = argparse.ArgumentParser(description="Record labelled 16 kHz mono WAV clips; human microphone required")
    parser.add_argument("--out", default="dataset")
    parser.add_argument("--speaker", required=True)
    parser.add_argument("--phrase", required=True, choices=sorted(CLASSES))
    parser.add_argument("--takes", type=int, default=40)
    parser.add_argument("--seconds", type=float, default=2.0)
    parser.add_argument("--distance-m", type=float, default=1.0)
    parser.add_argument("--room", default="unknown")
    parser.add_argument("--device")
    parser.add_argument("--yes", action="store_true", help="record without a prompt before every take")
    args = parser.parse_args()
    if args.takes <= 0 or args.seconds <= 0:
        parser.error("--takes and --seconds must be positive")
    try:
        import sounddevice as sd
    except ImportError:
        print("BLOCKED_HUMAN: install sounddevice and provide a working microphone; no audio was written")
        return 2

    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    metadata_path = out / "metadata.csv"
    rows = []
    if metadata_path.exists():
        with metadata_path.open(newline="") as stream:
            rows = list(csv.DictReader(stream))
    for take in range(1, args.takes + 1):
        if not args.yes:
            input(f"Take {take}/{args.takes}: press Enter, then say '{args.phrase}'...")
        frames = int(round(args.seconds * SAMPLE_RATE))
        recording = sd.rec(frames, samplerate=SAMPLE_RATE, channels=1, dtype="int16", device=args.device)
        sd.wait()
        samples = np.asarray(recording[:, 0], dtype=np.int16)
        clipped = bool(np.mean(np.abs(samples.astype(np.int32)) >= 32760) > 0.001)
        trimmed, start, end = _trim(samples)
        path = out / f"{args.speaker}_{args.phrase}_{take:03d}.wav"
        _write_wav(path, trimmed)
        rows.append({"path": str(path), "label": args.phrase, "speaker_id": args.speaker,
                     "distance_m": str(args.distance_m), "room": args.room, "sample_rate": str(SAMPLE_RATE),
                     "clipped": str(clipped).lower(), "trim_start": str(start), "trim_end": str(end)})
        print(json.dumps({"path": str(path), "clipped": clipped, "samples": len(trimmed)}))
    with metadata_path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    (out / "recording_provenance.json").write_text(json.dumps(
        generated_provenance({"speaker": args.speaker, "phrase": args.phrase, "takes": args.takes}), indent=2
    ) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
