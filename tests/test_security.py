from host.host_agent import dispatch
from host.protocol import Frame
from host.measurements import parse_meas
from pathlib import Path
import unittest

class SecurityTests(unittest.TestCase):
  def test_unknown_verb_rejected(self):
    self.assertEqual(dispatch(Frame(1, "RUN_SHELL", {"cmd": "echo bad"})).fields["code"], "verb_not_allowed")

  def test_path_is_project_id_only(self):
    self.assertEqual(dispatch(Frame(1, "OPEN_PROJECT", {"project": "../"})).verb, "ERR")

  def test_risky_action_requires_confirm(self):
    self.assertEqual(dispatch(Frame(1, "CLOSE_PROJECT", {})).fields["code"], "physical_confirm_required")

  def test_real_simulation_fails_closed_without_ngspice(self):
    result = dispatch(Frame(1, "RUN_SIMULATION", {"project": "amplifier"}))
    self.assertIn(result.verb, {"DONE", "ERR"})
    if result.verb == "ERR":
      self.assertEqual(result.fields["code"], "ngspice_unavailable")

  def test_measurement_parser_only_accepts_numeric_meas_lines(self):
    self.assertEqual(parse_meas("gain_db = -3.25\nbw_hz = 1200\nnoise = nope\n"), {"gain_db": -3.25, "bw_hz": 1200.0})

  def test_host_source_forbids_shell_true(self):
    source = "\n".join(path.read_text(errors="ignore") for path in Path("host").rglob("*.py"))
    self.assertNotIn("shell=True", source)
