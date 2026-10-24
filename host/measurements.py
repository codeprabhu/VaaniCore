"""Strict parser for ngspice .meas output; missing values stay missing."""
from __future__ import annotations
import re

MEAS = re.compile(r"^\s*([A-Za-z][A-Za-z0-9_]*)\s*=\s*([-+0-9.eE]+)")

def parse_meas(text: str) -> dict[str, float]:
    values: dict[str, float] = {}
    for line in text.splitlines():
        match = MEAS.match(line)
        if match:
            values[match.group(1)] = float(match.group(2))
    return values
