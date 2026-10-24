import json
import tempfile
import unittest
from pathlib import Path

from hardware.validate_pinmap import main as validate_pinmap


class HardwareCheckTests(unittest.TestCase):
    def test_pinmap_artifact_can_be_generated(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "pinmap.json"
            import sys
            old = sys.argv
            try:
                sys.argv = ["validate_pinmap", "--output", str(output)]
                self.assertEqual(validate_pinmap(), 0)
            finally:
                sys.argv = old
            self.assertEqual(json.loads(output.read_text())["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
