"""Virtual device: exercises framing and the host action loop without hardware."""
from __future__ import annotations
import argparse
from host.host_agent import dispatch
from host.intent_nlu import phrase_to_frame
from host.protocol import Frame, encode

def run() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", default="amplifier")
    parser.add_argument("--phrase", default="open the amplifier project and run the simulation")
    args = parser.parse_args()
    intent = phrase_to_frame(args.phrase, seq=2)
    if args.project != "amplifier" and intent.verb == "RUN_SIMULATION":
        intent = Frame(intent.seq, intent.verb, {**intent.fields, "project": args.project})
    for frame in (Frame(1, "PING", {}), intent, Frame(3, "RUN_SIMULATION", {"project": args.project})):
        if frame.verb == "ERR":
            print(encode(frame).decode().rstrip())
            continue
        print(encode(dispatch(frame, virtual=True)).decode().rstrip())

if __name__ == "__main__":
    run()
