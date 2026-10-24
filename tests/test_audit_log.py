import json
import tempfile
import unittest
from pathlib import Path
from host.audit_log import append_frame
from host.protocol import Frame

class AuditLogTests(unittest.TestCase):
    def test_jsonl_has_frame_metadata_and_no_audio_field(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "agent.jsonl"
            append_frame(path, "device_to_host", Frame(2, "PING", {"status": "ok"}))
            item = json.loads(path.read_text())
            self.assertEqual(item["verb"], "PING")
            self.assertNotIn("audio", item)
