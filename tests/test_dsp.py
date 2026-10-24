import unittest
from pathlib import Path
import numpy as np
from ml.features import mfcc_frame

class DspReferenceTests(unittest.TestCase):
    def test_golden_vector_is_reproducible(self):
        data = np.load(Path(__file__).parent / "vectors/mfcc_golden.npz")
        actual = mfcc_frame(data["samples"])
        self.assertLess(float(np.max(np.abs(actual - data["expected"]))), 1e-6)

    def test_shape(self):
        self.assertEqual(mfcc_frame(np.zeros(512, dtype=np.float32)).shape, (10,))

    def test_two_second_window_has_124_frames(self):
        from ml.features import mfcc
        self.assertEqual(mfcc(np.zeros(32000, dtype=np.float32)).shape, (124, 10))
