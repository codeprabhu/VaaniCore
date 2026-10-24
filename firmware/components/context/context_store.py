"""Host-testable reference for LAST/YESTERDAY context semantics."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import date

@dataclass
class Event:
    project_id: str
    action: str
    local_date: date

def resolve(events: list[Event], selector: str, today: date, confirmed_fallback: bool = False) -> Event | None:
    if not events:
        return None
    if selector == "LAST":
        return events[-1]
    if selector == "YESTERDAY":
        candidates = [e for e in reversed(events) if e.local_date == today.fromordinal(today.toordinal() - 1)]
        if len(candidates) == 1 or (candidates and confirmed_fallback):
            return candidates[0]
        if not candidates and confirmed_fallback:
            return events[-1]
        return None
    return next((e for e in events if e.project_id == selector), None)
