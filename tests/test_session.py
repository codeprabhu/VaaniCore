import unittest
from host.protocol import Frame
from host.session import HostSession

class SessionTests(unittest.TestCase):
    def test_connect_has_time_sync(self):
        frame = HostSession(virtual=True).connect_frames()[0]
        self.assertEqual(frame.verb, "TIME_SYNC")
        self.assertIn("epoch", frame.fields)

    def test_success_emits_ack_done_and_project_event(self):
        frames = HostSession(virtual=True).handle(Frame(4, "RUN_SIMULATION", {"project": "amplifier"}))
        self.assertEqual([frame.verb for frame in frames], ["ACK", "DONE", "PROJECT_EVENT"])

    def test_error_has_no_project_event(self):
        frames = HostSession(virtual=False).handle(Frame(4, "RUN_SIMULATION", {"project": "amplifier"}))
        self.assertEqual(frames[0].verb, "ACK")
        self.assertNotIn("PROJECT_EVENT", [frame.verb for frame in frames])
