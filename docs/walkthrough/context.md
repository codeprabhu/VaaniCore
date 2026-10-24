# Context-store walkthrough

`context_store.py` is the executable reference for the device's bounded event history. `device_protocol.py` consumes host `TIME_SYNC` and `PROJECT_EVENT` frames, converts epochs using the synchronized offset, and keeps the latest 16 events. `LAST` returns the newest event. `YESTERDAY` searches local dates, returns the sole candidate, and otherwise returns `None` so the UI can request confirmation; a confirmed fallback uses the latest event.

Viva questions: Why local date? The user says yesterday in local time. Why return `None`? Ambiguity must not trigger an action. Why keep events? To resolve references without cloud services. What is bounded on device? The firmware target is 16 events in NVS. What should change for timezone updates? Recompute local dates from the synchronized epoch before resolution.
