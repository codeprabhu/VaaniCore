import unittest
from ml.dataset import leave_one_speaker_out, summary

class DatasetTests(unittest.TestCase):
    def test_speakers_never_cross_split(self):
        rows = [{"path": "a.wav", "label": "open_amplifier", "speaker_id": "A", "distance_m": "1", "room": "lab"}, {"path": "b.wav", "label": "open_amplifier", "speaker_id": "B", "distance_m": "1", "room": "lab"}]
        splits = leave_one_speaker_out(rows)
        self.assertEqual(splits["A"], {"train": 1, "test": 1})
        self.assertEqual(summary(rows)["label"], "PIPELINE_METADATA_CHECK — NOT A RESULT")
