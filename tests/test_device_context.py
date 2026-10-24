import unittest
from datetime import date
from firmware.components.context.device_protocol import DeviceContext
from host.protocol import Frame

class DeviceProtocolContextTests(unittest.TestCase):
    def test_sync_and_project_event_resolve_local_day(self):
        context = DeviceContext()
        context.handle(Frame(1, "TIME_SYNC", {"epoch": "0", "tz_offset_min": "330"}))
        context.handle(Frame(2, "PROJECT_EVENT", {"epoch": "0", "project": "amplifier", "action": "RUN_SIMULATION"}))
        self.assertEqual(context.resolve("LAST", date(1970, 1, 1)).project_id, "amplifier")
        self.assertEqual(context.tz_offset_min, 330)

    def test_history_is_bounded(self):
        context = DeviceContext()
        for index in range(20):
            context.handle(Frame(index, "PROJECT_EVENT", {"epoch": str(index), "project": f"p{index}", "action": "OPEN_PROJECT"}))
        self.assertEqual(len(context.history), 16)
