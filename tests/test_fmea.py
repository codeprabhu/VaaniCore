import unittest
from pathlib import Path

from tools.validate_fmea import ROOT, validate


class FmeaTests(unittest.TestCase):
    def test_all_rows_have_evidence_mapping(self):
        self.assertEqual(validate(ROOT / "docs/FMEA.csv", ROOT / "docs/FMEA_TEST_MAP.csv"), [])


if __name__ == "__main__":
    unittest.main()
