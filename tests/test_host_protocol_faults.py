import unittest

from host.host_agent import _protocol_nack


class HostProtocolFaultTests(unittest.TestCase):
    def test_crc_fault_recovers_sequence_and_returns_nack(self):
        response = _protocol_nack(b"@37:PING0000\n", ValueError("CRC mismatch"))
        self.assertEqual((response.seq, response.verb, response.fields), (37, "NACK", {"reason": "crc"}))

    def test_malformed_fault_uses_zero_when_sequence_is_unrecoverable(self):
        response = _protocol_nack(b"garbage\n", ValueError("invalid frame"))
        self.assertEqual((response.seq, response.verb), (0, "NACK"))


if __name__ == "__main__":
    unittest.main()
