import unittest
import sys
import types
from host.transport import discover_port

class TransportTests(unittest.TestCase):
    def test_discovery_is_safe_without_serial_dependency(self):
        result = discover_port()
        self.assertTrue(result is None or isinstance(result, str))

    def test_serial_unplug_reconnects_and_repeats_handshake(self):
        import host.transport as transport
        original = sys.modules.get("serial")
        connections = []
        attempts = []

        class Reconnected:
            def __enter__(self): return self
            def __exit__(self, *_): return False
            def write(self, payload): connections.append(payload)
            def readline(self): raise KeyboardInterrupt

        def serial_factory(*_args, **_kwargs):
            attempts.append(True)
            if len(attempts) == 1:
                raise OSError("device unplugged")
            return Reconnected()

        sys.modules["serial"] = types.SimpleNamespace(Serial=serial_factory, SerialException=OSError)
        old_sleep = transport.time.sleep
        transport.time.sleep = lambda _seconds: None
        try:
            with self.assertRaises(KeyboardInterrupt):
                transport.serve_serial("/dev/fake", lambda line: b"ACK\n", on_connect=lambda: b"SYNC\n", reconnect_delay_s=0)
        finally:
            transport.time.sleep = old_sleep
            if original is None:
                sys.modules.pop("serial", None)
            else:
                sys.modules["serial"] = original
        self.assertEqual(connections, [b"SYNC\n"])
        self.assertEqual(len(attempts), 2)
