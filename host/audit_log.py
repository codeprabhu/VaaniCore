"""Append-only structured host-agent audit log; deliberately excludes raw audio."""
from __future__ import annotations
import json, pathlib, time
from host.protocol import Frame

def append_frame(path: str | pathlib.Path, direction: str, frame: Frame, error: str | None = None) -> None:
    target = pathlib.Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    event = {"epoch_s": time.time(), "direction": direction, "seq": frame.seq, "verb": frame.verb, "fields": frame.fields}
    if error:
        event["error"] = error
    with target.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(event, sort_keys=True) + "\n")
