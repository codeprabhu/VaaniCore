import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class MlEvalGateTests(unittest.TestCase):
    def test_missing_metadata_writes_non_result_status(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "eval.json"
            result = subprocess.run([sys.executable, "ml/eval.py", "--output", str(output)], check=False, capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            data = json.loads(output.read_text())
            self.assertEqual(data["status"], "BLOCKED_INPUT")
            self.assertEqual(data["label"], "NOT_A_RESULT")


if __name__ == "__main__":
    unittest.main()
