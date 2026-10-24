import unittest
from pathlib import Path
from tools.audit_phase_a import ROOT

class AuditTests(unittest.TestCase):
    def test_audit_script_and_inputs_exist(self):
        self.assertTrue((ROOT / "tools/audit_phase_a.py").is_file())
        self.assertTrue((ROOT / "inputs/vishwakarma.pdf").is_file())
