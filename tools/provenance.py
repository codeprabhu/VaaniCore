"""Small provenance helper for generated artifacts; never shells out through a command string."""
from __future__ import annotations
from datetime import datetime, timezone
import pathlib, subprocess

ROOT = pathlib.Path(__file__).resolve().parents[1]

def generated_provenance(config: object = None) -> dict[str, object]:
    try:
        commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=False, capture_output=True, text=True).stdout.strip() or "unknown"
    except OSError:
        commit = "unknown"
    return {"generated_at_utc": datetime.now(timezone.utc).isoformat(), "git_commit": commit, "config": config}
