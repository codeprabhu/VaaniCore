"""Run the hardware-free virtual benchmark with explicit SIMULATED provenance."""
from __future__ import annotations
import argparse, csv, json, pathlib, statistics, time, sys
try:
    from host.host_agent import dispatch
    from host.intent_nlu import phrase_to_frame
    from host.protocol import encode
except ModuleNotFoundError:
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
    from host.host_agent import dispatch
    from host.intent_nlu import phrase_to_frame
    from host.protocol import encode

def percentile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, int(round((len(ordered) - 1) * fraction))))
    return ordered[index]

def distribution(values: list[float]) -> dict[str, object]:
    return {"median": statistics.median(values), "p95": percentile(values, 0.95), "iqr": percentile(values, 0.75) - percentile(values, 0.25), "n": len(values), "label": "SIMULATED"}

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate labelled virtual P1 benchmark evidence")
    parser.add_argument("--output", default="results/summary.json")
    parser.add_argument("--trials", type=int, default=30)
    args = parser.parse_args()
    if args.trials < 30:
        raise SystemExit("--trials must be at least 30")
    rows = []
    latencies = []
    bytes_sent = []
    for trial in range(1, args.trials + 1):
        start = time.perf_counter_ns()
        intent = phrase_to_frame("open the amplifier project and run the simulation", seq=trial % 256)
        request = encode(intent)
        response = dispatch(intent, virtual=True)
        elapsed_ms = (time.perf_counter_ns() - start) / 1_000_000
        latencies.append(elapsed_ms); bytes_sent.append(len(request))
        rows.append({"trial": trial, "condition": "SIMULATED_P1", "latency_ms": elapsed_ms, "usb_bytes": len(request), "success": response.verb == "DONE", "label": "SIMULATED"})
    output = pathlib.Path(args.output); output.parent.mkdir(parents=True, exist_ok=True)
    csv_path = output.with_name("virtual_trials.csv")
    with csv_path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0]); writer.writeheader(); writer.writerows(rows)
    data = {"provenance": {"label": "SIMULATED", "condition": "SIMULATED_PIPELINE_TEST", "n": args.trials, "source": str(csv_path), "note": "Virtual device only; never a hardware result."}, "metrics": {
        "virtual_success_rate": {"value": sum(row["success"] for row in rows) / args.trials, "label": "SIMULATED", "n": args.trials},
        "virtual_latency_ms": distribution(latencies),
        "virtual_usb_bytes": distribution([float(value) for value in bytes_sent]),
        "inference_ms": {"value": 100, "label": "TARGET"}, "e2e_latency_ms": {"value": 500, "label": "TARGET"},
        "usb_bytes_p1": {"value": 80, "label": "TARGET"}, "usb_bytes_p2": {"value": 64000, "label": "TARGET"},
        "host_idle_cpu_percent": {"value": None, "label": "TARGET"}, "average_power_w": {"value": 0.6, "label": "TARGET"}
    }}
    output.write_text(json.dumps(data, indent=2) + "\n")
    print(output)

if __name__ == "__main__":
    main()
