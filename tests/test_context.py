import unittest
from datetime import date, timedelta
from firmware.components.context.context_store import Event, resolve

class ContextTests(unittest.TestCase):
    def setUp(self):
        self.today = date(2026, 10, 24)
        self.events = [Event("filter", "OPEN_PROJECT", self.today - timedelta(days=1)), Event("amplifier", "RUN_SIMULATION", self.today)]

    def test_last(self):
        self.assertEqual(resolve(self.events, "LAST", self.today).project_id, "amplifier")

    def test_yesterday(self):
        self.assertEqual(resolve(self.events, "YESTERDAY", self.today).project_id, "filter")

    def test_missing_yesterday_requires_confirmation(self):
        events = [Event("amplifier", "RUN_SIMULATION", self.today)]
        self.assertIsNone(resolve(events, "YESTERDAY", self.today))
        self.assertEqual(resolve(events, "YESTERDAY", self.today, True).project_id, "amplifier")
