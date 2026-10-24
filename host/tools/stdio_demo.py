"""Exercise the real host-agent stdio service with virtual project actions."""
from __future__ import annotations

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from host.protocol import Frame, decode, encode


def main() -> int:
    requests = [Frame(1, "PING", {}), Frame(2, "RUN_SIMULATION", {"project": "amplifier"})]
    corrupted = bytearray(encode(Frame(9, "PING", {})))
    corrupted[-5] = ord("0")
    payload = b"".join(encode(frame) for frame in requests) + bytes(corrupted)
    command = [sys.executable, str(ROOT / "host/host_agent.py"), "--stdio", "--virtual", "--log", "/tmp/vaanicore_stdio.jsonl"]
    completed = subprocess.run(command, input=payload, capture_output=True, check=False)
    if completed.returncode != 0:
        raise SystemExit(completed.stderr.decode(errors="replace"))
    responses = [decode(line) for line in completed.stdout.splitlines(keepends=True) if line]
    verbs = [frame.verb for frame in responses]
    expected = ["ACK", "DONE", "ACK", "DONE", "PROJECT_EVENT", "NACK"]
    if verbs != expected:
        raise SystemExit(f"unexpected host-agent response sequence: {verbs!r}")
    print("stdio host-agent loop passed: " + " ".join(verbs))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
