"""Generate only labelled virtual benchmark evidence; never masquerades as hardware data."""
from __future__ import annotations
import argparse, json, pathlib, time
from host.host_agent import dispatch
from host.protocol import Frame

def main():
    p = argparse.ArgumentParser(); p.add_argument("--output", default="results/summary.json"); args = p.parse_args()
    started = time.time(); responses = [dispatch(Frame(i, "RUN_SIMULATION", {"project": "amplifier"})) for i in range(1, 31)]
    data = {"provenance": {"label": "SIMULATED", "condition": "SIMULATED_PIPELINE_TEST", "n": 30, "duration_s": time.time()-started}, "metrics": {
        "virtual_success_rate": {"value": sum(r.verb == "DONE" for r in responses)/30, "label": "SIMULATED"},
        "inference_ms": {"value": 100, "label": "TARGET"}, "e2e_latency_ms": {"value": 500, "label": "TARGET"},
        "usb_bytes_p1": {"value": 80, "label": "TARGET"}, "usb_bytes_p2": {"value": 64000, "label": "TARGET"},
        "host_idle_cpu_percent": {"value": None, "label": "TARGET"}, "average_power_w": {"value": 0.6, "label": "TARGET"}
    }}
    path = pathlib.Path(args.output); path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(data, indent=2) + "\n")
    print(path)
if __name__ == "__main__": main()
