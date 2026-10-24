"""Analyze manual-vs-voice timing data while refusing placeholder rows."""
from __future__ import annotations
import argparse, csv, json, pathlib, statistics
from tools.provenance import generated_provenance

def analyze(path: pathlib.Path) -> dict[str, object]:
    with path.open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    valid = []
    for row in rows:
        try:
            seconds = float(row["seconds"]); actions = float(row["ui_actions"])
        except (KeyError, TypeError, ValueError):
            continue
        if seconds >= 0 and actions >= 0 and row.get("condition") in {"manual", "voice"}:
            valid.append({"condition": row["condition"], "seconds": seconds, "actions": actions})
    if not valid:
        return {"provenance": generated_provenance({"input": str(path)}), "status": "BLOCKED_HUMAN", "label": "NOT_A_RESULT", "reason": "numeric manual and voice timing rows are required", "input": str(path)}
    grouped = {}
    for condition in ("manual", "voice"):
        values = [row for row in valid if row["condition"] == condition]
        if values:
            grouped[condition] = {"n": len(values), "median_seconds": statistics.median(row["seconds"] for row in values), "median_ui_actions": statistics.median(row["actions"] for row in values)}
    result = {"provenance": generated_provenance({"input": str(path)}), "status": "MEASURED", "label": "MEASURED", "input": str(path), "conditions": grouped}
    if "manual" in grouped and "voice" in grouped:
        result["seconds_reduction_percent"] = 100 * (1 - grouped["voice"]["median_seconds"] / grouped["manual"]["median_seconds"]) if grouped["manual"]["median_seconds"] else None
    return result

def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze timing-study CSV")
    parser.add_argument("--input", default="bench/timing_study.csv")
    parser.add_argument("--output", default="results/timing_study_status.json")
    args = parser.parse_args()
    result = analyze(pathlib.Path(args.input)); output = pathlib.Path(args.output); output.parent.mkdir(parents=True, exist_ok=True); output.write_text(json.dumps(result, indent=2) + "\n"); print(output)
if __name__ == "__main__": main()
