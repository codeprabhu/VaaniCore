"""Reference VaaniCore framing codec; no shell or device input is executed."""
from __future__ import annotations
import re
from dataclasses import dataclass

MAX_FRAME = 128
_BODY = re.compile(r"^@(?P<seq>\d+):(?P<verb>[A-Z_]+)(?::(?P<fields>[^*]*))?$")

def crc16(data: bytes) -> int:
    value = 0xFFFF
    for byte in data:
        value ^= byte << 8
        for _ in range(8):
            value = ((value << 1) ^ 0x1021) & 0xFFFF if value & 0x8000 else (value << 1) & 0xFFFF
    return value

@dataclass(frozen=True)
class Frame:
    seq: int
    verb: str
    fields: dict[str, str]

def encode(frame: Frame) -> bytes:
    fields = ",".join(f"{k}={v}" for k, v in sorted(frame.fields.items()))
    body = f"@{frame.seq % 256}:{frame.verb}" + (f":{fields}" if fields else "")
    result = f"{body}{crc16(body.encode()):04X}\n".encode()
    if len(result) > MAX_FRAME:
        raise ValueError("frame exceeds 128 bytes")
    return result

def decode(raw: bytes | str) -> Frame:
    if isinstance(raw, bytes):
        raw = raw.decode("ascii")
    if len(raw.encode()) > MAX_FRAME or not raw.endswith("\n"):
        raise ValueError("invalid frame length or terminator")
    line = raw[:-1]
    if len(line) < 6:
        raise ValueError("short frame")
    body, supplied = line[:-4], line[-4:]
    if not re.fullmatch(r"[0-9A-Fa-f]{4}", supplied) or crc16(body.encode()) != int(supplied, 16):
        raise ValueError("CRC mismatch")
    match = _BODY.fullmatch(body)
    if not match:
        raise ValueError("invalid frame body")
    fields = {}
    if match.group("fields"):
        for item in match.group("fields").split(","):
            key, sep, value = item.partition("=")
            if not sep or not re.fullmatch(r"[a-z][a-z0-9_]*", key):
                raise ValueError("invalid field")
            fields[key] = value
    return Frame(int(match.group("seq")) % 256, match.group("verb"), fields)
