"""Host-testable device-side handling of TIME_SYNC and PROJECT_EVENT frames."""
from __future__ import annotations
from datetime import date, datetime, timedelta, timezone
from host.protocol import Frame
from firmware.components.context.context_store import Event, resolve

class DeviceContext:
    def __init__(self) -> None:
        self.tz_offset_min = 0
        self.history: list[Event] = []

    def handle(self, frame: Frame) -> None:
        if frame.verb == "TIME_SYNC":
            self.tz_offset_min = int(frame.fields["tz_offset_min"])
        elif frame.verb == "PROJECT_EVENT":
            epoch = int(frame.fields["epoch"])
            local_zone = timezone(timedelta(minutes=self.tz_offset_min))
            local_day = datetime.fromtimestamp(epoch, tz=timezone.utc).astimezone(local_zone).date()
            self.history.append(Event(frame.fields["project"], frame.fields.get("action", ""), local_day))
            self.history = self.history[-16:]

    def resolve(self, selector: str, today: date, confirmed_fallback: bool = False) -> Event | None:
        return resolve(self.history, selector, today, confirmed_fallback)
