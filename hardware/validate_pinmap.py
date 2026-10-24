from __future__ import annotations
import argparse, csv, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from tools.provenance import generated_provenance

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default="hardware/pinmap.csv")
    parser.add_argument("--output", default="results/pinmap_validation.json")
    args = parser.parse_args()
    with open(args.csv, newline="") as stream:
        rows = list(csv.DictReader(stream))
    gpios = [int(r["gpio"]) for r in rows]
    errors = []
    if len(gpios) != len(set(gpios)): errors.append("duplicate GPIO")
    if any(26 <= x <= 37 for x in gpios): errors.append("flash/PSRAM GPIO used")
    if any(x in {0, 3, 45, 46} for x in gpios): errors.append("strapping GPIO used")
    if {19, 20} - set(gpios): errors.append("USB GPIO missing")
    if errors: raise SystemExit("; ".join(errors))
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"provenance": generated_provenance({"input": args.csv}),
                                  "status": "PASS", "label": "DESIGN_VALIDATION",
                                  "pins": len(rows)}, indent=2) + "\n")
    print(f"validated {len(rows)} pins; {output}")
    return 0
if __name__ == "__main__": raise SystemExit(main())
