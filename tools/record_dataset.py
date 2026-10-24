"""Human-operated recording tool interface; it refuses to invent audio."""
from __future__ import annotations
import argparse, pathlib

def main():
    p=argparse.ArgumentParser(description="Record labelled 16 kHz mono WAV clips (hardware/input required)")
    p.add_argument("--out", default="dataset"); p.add_argument("--speaker", required=True); p.add_argument("--phrase", required=True); p.add_argument("--takes", type=int, default=40); a=p.parse_args()
    pathlib.Path(a.out).mkdir(parents=True, exist_ok=True)
    print(f"READY: human recording required for speaker={a.speaker!r}, phrase={a.phrase!r}, takes={a.takes}; no files created")
if __name__ == '__main__': main()
