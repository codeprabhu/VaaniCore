from __future__ import annotations
import argparse, csv, pathlib

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default="hardware/pinmap.csv")
    args = parser.parse_args()
    rows = list(csv.DictReader(open(args.csv, newline="")))
    gpios = [int(r["gpio"]) for r in rows]
    errors = []
    if len(gpios) != len(set(gpios)): errors.append("duplicate GPIO")
    if any(26 <= x <= 37 for x in gpios): errors.append("flash/PSRAM GPIO used")
    if any(x in {0, 3, 45, 46} for x in gpios): errors.append("strapping GPIO used")
    if {19, 20} - set(gpios): errors.append("USB GPIO missing")
    if errors: raise SystemExit("; ".join(errors))
    print(f"validated {len(rows)} pins")
    return 0
if __name__ == "__main__": raise SystemExit(main())
