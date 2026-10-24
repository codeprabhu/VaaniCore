from host.host_agent import dispatch
from host.protocol import Frame
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
