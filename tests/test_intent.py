import unittest
from host.intent_nlu import phrase_to_frame

class IntentTests(unittest.TestCase):
    def test_supported_phrase(self):
        frame = phrase_to_frame("Open the amplifier project and run the simulation")
        self.assertEqual((frame.verb, frame.fields["project"]), ("RUN_SIMULATION", "amplifier"))
        self.assertEqual(frame.fields["open"], "1")

    def test_unknown_phrase_never_becomes_action(self):
        self.assertEqual(phrase_to_frame("delete everything").verb, "ERR")
