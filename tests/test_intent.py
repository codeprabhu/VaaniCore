import unittest
from host.intent_nlu import phrase_to_frame

class IntentTests(unittest.TestCase):
    def test_supported_phrase(self):
        frame = phrase_to_frame("Open the amplifier project and run the simulation")
        self.assertEqual((frame.verb, frame.fields["project"]), ("RUN_SIMULATION", "amplifier"))
        self.assertEqual(frame.fields["open"], "1")

    def test_unknown_phrase_never_becomes_action(self):
        self.assertEqual(phrase_to_frame("delete everything").verb, "ERR")

    def test_all_control_intents_are_typed(self):
        cases = {
            "open the regulator project": ("OPEN_PROJECT", "regulator"),
            "open yesterday's project": ("OPEN_PROJECT", "YESTERDAY"),
            "open the last project": ("OPEN_PROJECT", "LAST"),
            "show the result": ("SHOW_RESULT", None),
            "cancel": ("CANCEL", None),
            "confirm": ("CONFIRM", None),
            "close the project": ("CLOSE_PROJECT", "LAST"),
            "run simulation": ("RUN_SIMULATION", "LAST"),
        }
        for phrase, (verb, project) in cases.items():
            frame = phrase_to_frame(phrase)
            self.assertEqual(frame.verb, verb, phrase)
            if project is not None:
                self.assertEqual(frame.fields["project"], project, phrase)
