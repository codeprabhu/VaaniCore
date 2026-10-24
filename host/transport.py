"""Optional serial transport with bounded, line-oriented reads."""
from __future__ import annotations
import argparse

def discover_port() -> str | None:
    try:
        from serial.tools import list_ports
    except ImportError:
        return None
    candidates = [port.device for port in list_ports.comports() if port.vid in {0x303A, 0x1209} or "Vaani" in (port.description or "")]
    return candidates[0] if len(candidates) == 1 else None

def serve_serial(port: str, handler, baud: int = 115200, on_connect=None) -> None:
    try:
        import serial
    except ImportError as exc:
        raise RuntimeError("pyserial is required for --port; use --stdio for the virtual transport") from exc
    with serial.Serial(port, baudrate=baud, timeout=0.5) as device:
        if on_connect:
            device.write(on_connect())
        while True:
            line = device.readline()
            if not line:
                continue
            device.write(handler(line))
