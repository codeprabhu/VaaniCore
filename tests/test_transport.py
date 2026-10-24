import unittest
from host.transport import discover_port

class TransportTests(unittest.TestCase):
    def test_discovery_is_safe_without_serial_dependency(self):
        result = discover_port()
        self.assertTrue(result is None or isinstance(result, str))
