"""Closed-vocabulary phrase-to-intent mapping used by the virtual path."""
from __future__ import annotations
import re
from host.protocol import Frame

def phrase_to_frame(phrase: str, seq: int = 1) -> Frame:
    normalized = re.sub(r"[^a-z0-9 ]", "", phrase.lower()).strip()
    if normalized in {"cancel", "cancel that", "stop"}:
        return Frame(seq, "CANCEL", {})
    if normalized in {"confirm", "yes", "do it"}:
        return Frame(seq, "CONFIRM", {})
    if "close" in normalized and "project" in normalized:
        return Frame(seq, "CLOSE_PROJECT", {"project": "LAST"})
    if "show" in normalized and "result" in normalized:
        return Frame(seq, "SHOW_RESULT", {})
    if "yesterday" in normalized and "run" in normalized:
        return Frame(seq, "RUN_SIMULATION", {"project": "filter", "context": "YESTERDAY", "open": "1"})
    if "amplifier" in normalized and "run" in normalized:
        return Frame(seq, "RUN_SIMULATION", {"project": "amplifier", "open": "1"})
    if "regulator" in normalized and normalized.startswith("open"):
        return Frame(seq, "OPEN_PROJECT", {"project": "regulator"})
    if normalized.startswith("open amplifier"):
        return Frame(seq, "OPEN_PROJECT", {"project": "amplifier"})
    if normalized.startswith("open filter"):
        return Frame(seq, "OPEN_PROJECT", {"project": "filter"})
    if normalized.startswith("open") and "yesterday" in normalized:
        return Frame(seq, "OPEN_PROJECT", {"project": "YESTERDAY", "context": "YESTERDAY"})
    if normalized.startswith("open") and "last" in normalized:
        return Frame(seq, "OPEN_PROJECT", {"project": "LAST", "context": "LAST"})
    if normalized.startswith("run simulation"):
        return Frame(seq, "RUN_SIMULATION", {"project": "LAST", "context": "LAST"})
    return Frame(seq, "ERR", {"code": "unrecognised_intent"})
