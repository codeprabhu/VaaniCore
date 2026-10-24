"""Closed-vocabulary phrase-to-intent mapping used by the virtual path."""
from __future__ import annotations
import re
from host.protocol import Frame

def phrase_to_frame(phrase: str, seq: int = 1) -> Frame:
    normalized = re.sub(r"[^a-z0-9 ]", "", phrase.lower()).strip()
    if "yesterday" in normalized and "run" in normalized:
        return Frame(seq, "RUN_SIMULATION", {"project": "filter", "context": "YESTERDAY", "open": "1"})
    if "amplifier" in normalized and "run" in normalized:
        return Frame(seq, "RUN_SIMULATION", {"project": "amplifier", "open": "1"})
    if normalized.startswith("open amplifier"):
        return Frame(seq, "OPEN_PROJECT", {"project": "amplifier"})
    if normalized.startswith("open filter"):
        return Frame(seq, "OPEN_PROJECT", {"project": "filter"})
    return Frame(seq, "ERR", {"code": "unrecognised_intent"})
