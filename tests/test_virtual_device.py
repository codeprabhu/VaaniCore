import unittest

from datetime import date

from firmware.components.context.device_protocol import DeviceContext
from host.protocol import Frame
from host.session import HostSession


class VirtualLifecycleTests(unittest.TestCase):
    def test_session_sync_and_event_update_device_context(self):
        device = DeviceContext()
        session = HostSession(virtual=True)
        for frame in session.connect_frames():
            device.handle(frame)
        responses = session.handle(Frame(7, "RUN_SIMULATION", {"project": "amplifier"}))
        for frame in responses:
            device.handle(frame)
        self.assertEqual(device.history[-1].project_id, "amplifier")
        self.assertEqual(device.history[-1].action, "RUN_SIMULATION")
        self.assertEqual(device.resolve("LAST", date.today()).project_id, "amplifier")


if __name__ == "__main__":
    unittest.main()
