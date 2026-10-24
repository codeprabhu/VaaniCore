"""Connection lifecycle and response sequencing for the USB host agent."""
from __future__ import annotations
from datetime import datetime, timezone
import time
from host.protocol import Frame

class HostSession:
    def __init__(self, virtual: bool = False):
        self.virtual = virtual
        self.next_seq = 1

    def time_sync(self) -> Frame:
        local = datetime.now().astimezone()
        offset = int(local.utcoffset().total_seconds() // 60) if local.utcoffset() else 0
        return Frame(self.next_seq % 256, "TIME_SYNC", {"epoch": str(int(time.time())), "tz_offset_min": str(offset)})

    def connect_frames(self) -> list[Frame]:
        frame = self.time_sync()
        self.next_seq += 1
        return [frame]

    def handle(self, request: Frame, confirm: bool = False) -> list[Frame]:
        from host.host_agent import dispatch
        ack = Frame(request.seq, "ACK", {"seq": str(request.seq)})
        response = dispatch(request, confirm=confirm, virtual=self.virtual)
        frames = [ack, response]
        if response.verb == "DONE" and response.fields.get("project") and request.verb in {"OPEN_PROJECT", "RUN_SIMULATION"}:
            frames.append(Frame(request.seq, "PROJECT_EVENT", {"action": request.verb, "project": response.fields["project"], "epoch": str(int(time.time()))}))
        return frames
