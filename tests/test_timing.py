import csv
import json
import tempfile
import unittest
from pathlib import Path
from bench.analyze_timing import analyze

class TimingTests(unittest.TestCase):
    def test_placeholder_is_blocked(self):
        result = analyze(Path("bench/timing_study.csv"))
        self.assertEqual(result["status"], "BLOCKED_HUMAN")

    def test_numeric_rows_produce_measured_summary(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "timing.csv"
            with path.open("w", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=["participant", "condition", "trial", "seconds", "ui_actions"]); writer.writeheader()
                writer.writerows([{"participant": "A", "condition": "manual", "trial": 1, "seconds": 10, "ui_actions": 5}, {"participant": "A", "condition": "voice", "trial": 1, "seconds": 4, "ui_actions": 1}])
            result = analyze(path)
            self.assertEqual(result["status"], "MEASURED")
            self.assertEqual(result["seconds_reduction_percent"], 60.0)
