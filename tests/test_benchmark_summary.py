import json
import tempfile
import unittest
from pathlib import Path

from bench.validate_summary import validate


class BenchmarkSummaryTests(unittest.TestCase):
    def test_current_summary_has_required_schema(self):
        self.assertEqual(validate(Path("results/summary.json")), [])

    def test_missing_metric_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "summary.json"
            path.write_text(json.dumps({"provenance": {"label": "SIMULATED", "source": "x", "n": 30}, "metrics": {}}))
            self.assertTrue(validate(path))


if __name__ == "__main__":
    unittest.main()
