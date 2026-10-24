from host.protocol import Frame, crc16, decode, encode
import unittest
import json
from pathlib import Path

class ProtocolTests(unittest.TestCase):
  def test_crc_known_vector(self):
    self.assertEqual(crc16(b"123456789"), 0x29B1)

  def test_round_trip(self):
    frame = Frame(7, "RUN_SIMULATION", {"project": "amplifier"})
    self.assertEqual(decode(encode(frame)), frame)

  def test_corruption_rejected(self):
    raw = encode(Frame(1, "PING", {}))
    with self.assertRaisesRegex(ValueError, "CRC"):
        decode(raw[:-5] + b"0" + raw[-4:])

  def test_oversize_rejected(self):
    with self.assertRaises(ValueError):
        encode(Frame(1, "PING", {"x": "a" * 200}))

  def test_shared_vectors(self):
    vectors = json.loads((Path(__file__).parent / "protocol/vectors.json").read_text())
    for vector in vectors:
      self.assertEqual(decode(vector["frame"]).verb, vector["verb"])
      self.assertEqual(encode(Frame(vector["seq"], vector["verb"], vector["fields"])).decode(), vector["frame"])

  def test_fuzz_rejects_or_parses_without_crashing(self):
    for raw in (b"", b"garbage\n", b"@1:PING0000\n", b"\xff\xff\n", b"@999:"):
      try:
        decode(raw)
      except (ValueError, UnicodeDecodeError):
        pass
