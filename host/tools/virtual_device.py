"""Virtual device: exercises framing and the host action loop without hardware."""
from __future__ import annotations
import argparse
from host.host_agent import dispatch
from host.protocol import Frame, encode

def run() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", default="amplifier")
    args = parser.parse_args()
    for frame in (Frame(1, "PING", {}), Frame(2, "OPEN_PROJECT", {"project": args.project}), Frame(3, "RUN_SIMULATION", {"project": args.project})):
        print(encode(dispatch(frame, virtual=True)).decode().rstrip())

if __name__ == "__main__":
    run()
