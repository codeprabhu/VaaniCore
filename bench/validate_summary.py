"""Validate benchmark artifact shape without upgrading targets/simulations into results."""
from __future__ import annotations

import argparse
import json
import pathlib

ALLOWED_LABELS = {"TARGET", "ESTIMATE", "SIMULATED", "MEASURED"}
REQUIRED_METRICS = {"inference_ms", "e2e_latency_ms", "usb_bytes_p1", "usb_bytes_p2", "host_idle_cpu_percent", "average_power_w"}


def validate(path: pathlib.Path) -> list[str]:
    errors = []
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        return [f"summary unreadable: {exc}"]
    provenance = data.get("provenance", {})
    if provenance.get("label") not in ALLOWED_LABELS:
        errors.append("provenance.label must be an allowed evidence label")
    if not provenance.get("source"):
        errors.append("provenance.source is required")
    if not isinstance(provenance.get("n"), int) or provenance["n"] < 30:
        errors.append("provenance.n must be an integer >= 30")
    metrics = data.get("metrics")
    if not isinstance(metrics, dict) or len(metrics) < 6:
        errors.append("at least six metrics are required")
        return errors
    missing = REQUIRED_METRICS - set(metrics)
    if missing:
        errors.append(f"missing required metrics: {sorted(missing)}")
    for name, metric in metrics.items():
        if not isinstance(metric, dict) or metric.get("label") not in ALLOWED_LABELS:
            errors.append(f"metric {name!r} lacks an allowed label")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate VaaniCore benchmark summary schema")
    parser.add_argument("--input", default="results/summary.json")
    args = parser.parse_args()
    errors = validate(pathlib.Path(args.input))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 2
    print(f"benchmark summary valid: {args.input}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
