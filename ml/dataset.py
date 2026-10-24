"""Metadata-only dataset checks; does not manufacture audio or evaluation scores."""
from __future__ import annotations
import csv
from collections import Counter

REQUIRED = {"path", "label", "speaker_id", "distance_m", "room"}

def read_metadata(path: str) -> list[dict[str, str]]:
    with open(path, newline="") as stream:
        rows = list(csv.DictReader(stream))
    missing = REQUIRED - set(rows[0]) if rows else REQUIRED
    if missing:
        raise ValueError(f"metadata missing columns: {sorted(missing)}")
    return rows

def leave_one_speaker_out(rows: list[dict[str, str]]) -> dict[str, dict[str, int]]:
    speakers = sorted({row["speaker_id"] for row in rows})
    return {held_out: {"train": sum(row["speaker_id"] != held_out for row in rows), "test": sum(row["speaker_id"] == held_out for row in rows)} for held_out in speakers}

def summary(rows: list[dict[str, str]]) -> dict[str, object]:
    return {"clips": len(rows), "speakers": dict(Counter(row["speaker_id"] for row in rows)), "labels": dict(Counter(row["label"] for row in rows)), "splits": leave_one_speaker_out(rows), "label": "PIPELINE_METADATA_CHECK — NOT A RESULT"}
