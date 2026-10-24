"""Validate that every FMEA row has a traceable test/evidence mapping."""
from __future__ import annotations

import argparse
import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]


def validate(fmea_path: pathlib.Path, map_path: pathlib.Path) -> list[str]:
    errors = []
    with fmea_path.open(newline="") as stream:
        fmea = list(csv.DictReader(stream))
    with map_path.open(newline="") as stream:
        mapping = {row["test_id"]: row for row in csv.DictReader(stream)}
    ids = set()
    for row in fmea:
        row_id = row.get("id", "")
        test_id = row.get("test_id", "")
        if not row_id or row_id in ids:
            errors.append(f"duplicate or empty FMEA id: {row_id!r}")
        ids.add(row_id)
        if not test_id or test_id not in mapping:
            errors.append(f"{row_id}: missing test mapping for {test_id!r}")
            continue
        evidence = mapping[test_id].get("evidence", "")
        path = evidence.split("::", 1)[0]
        if not (ROOT / path).exists():
            errors.append(f"{row_id}: evidence path does not exist: {path}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate VaaniCore FMEA test/evidence mappings")
    parser.add_argument("--fmea", default="docs/FMEA.csv")
    parser.add_argument("--map", dest="mapping", default="docs/FMEA_TEST_MAP.csv")
    args = parser.parse_args()
    errors = validate(ROOT / args.fmea, ROOT / args.mapping)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 2
    print(f"FMEA mapping valid: {args.fmea}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
