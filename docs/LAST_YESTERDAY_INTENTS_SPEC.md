# LAST and YESTERDAY Intents Specification

**Generated:** 2026-11-19T01:35:00Z
**Git Commit:** ae1c35e
**Status:** APPROVED

---

## Contract

**Scope:** Context-aware intent resolution for LAST and YESTERDAY selectors in host and firmware.

**Purpose:** Enable voice commands like "run last simulation" or "open yesterday's project" with deterministic resolution.

---

## Python Intent Mapping (`host/intent_nlu.py`)

### Phrase Patterns
| Phrase Pattern | Intent Frame |
|----------------|--------------|
| "yesterday" + "run" | `RUN_SIMULATION`, `{project: "filter", context: "YESTERDAY", open: "1"}` |
| "amplifier" + "run" | `RUN_SIMULATION`, `{project: "amplifier", open: "1"}` |
| "open" + "yesterday" | `OPEN_PROJECT`, `{project: "YESTERDAY", context: "YESTERDAY"}` |
| "open" + "last" | `OPEN_PROJECT`, `{project: "LAST", context: "LAST"}` |
| "run simulation" (no project) | `RUN_SIMULATION`, `{project: "LAST", context: "LAST"}` |

### Resolution in Host
Host `dispatch()` receives frame with `project="LAST"` or `"YESTERDAY"`:
1. Calls `_project(selector)` which validates against PROJECTS dict
2. For LAST/YESTERDAY: resolves via `ContextStore.resolve(selector, today, confirmed_fallback)`
3. Uses resolved `project_id` for actual action

---

## Firmware Intent Table (`firmware/main/intents.c`)

```c
static const vc_intent_t INTENTS[] = {
    {"open_amplifier", "OPEN_PROJECT", "amplifier", 0, 0},
    {"open_filter", "OPEN_PROJECT", "filter", 0, 0},
    {"open_regulator", "OPEN_PROJECT", "regulator", 0, 0},
    {"open_last", "OPEN_PROJECT", "LAST", 0, 0},
    {"open_yesterday", "OPEN_PROJECT", "YESTERDAY", 0, 0},
    {"run_sim", "RUN_SIMULATION", "LAST", 0, 0},
    {"open_amp_run_sim", "RUN_SIMULATION", "amplifier", 0, 1},
    {"open_yday_run_sim", "RUN_SIMULATION", "YESTERDAY", 0, 1},
    {"show_result", "SHOW_RESULT", "LAST", 0, 0},
    {"cancel", "CANCEL", "", 0, 0},
    {"confirm", "CONFIRM", "", 0, 0},
    {"close_project", "CLOSE_PROJECT", "LAST", 1, 0},  // risky=1
    {"_unknown_", "", "", 0, 0},
    {"_silence_", "", "", 0, 0},
};
```

### Fields
- `class_name`: Classifier output label
- `verb`: Protocol verb
- `project`: Project ID or LAST/YESTERDAY
- `risky`: 1 if requires confirmation (CLOSE_PROJECT)
- `open`: 1 if should open project before simulation

---

## Resolution Logic

### Host (Python)
```python
# In _project() or dispatch()
if project_id in {"LAST", "YESTERDAY"}:
    event = context_store.resolve(project_id, today, confirmed_fallback)
    if event:
        project_id = event["project_id"]
    else:
        raise ValueError("invalid_project_id")
```

### Firmware (C)
```c
// In intent handling task
const vc_intent_t *intent = vc_intent_lookup(class_name);
if (intent && (strcmp(intent->project, "LAST") == 0 || strcmp(intent->project, "YESTERDAY") == 0)) {
    vc_event_t event;
    if (vc_history_resolve_confirmed(&history, intent->project, local_day, &event)) {
        // Use event.project_id for action
    }
}
```

---

## Confirmation Fallback

### Host
```python
# YESTERDAY with no unique match
event = context_store.resolve("YESTERDAY", today, confirmed_fallback=False)
if not event:
    # Return ERR, device must send CONFIRM then retry
    return ERR:physical_confirm_required
# With confirm:
event = context_store.resolve("YESTERDAY", today, confirmed_fallback=True)
```

### Firmware
- `vc_history_resolve_confirmed()` implements fallback
- Device sends CONFIRM frame (GPIO15 press) before retry

---

## Invariants

1. **Host resolves before dispatch** — LAST/YESTERDAY never sent to device in frames
2. **Firmware resolves on device** — Classifier outputs LAST/YESTERDAY, device resolves
3. **YESTERDAY requires uniqueness** — Multiple events same day → None (without fallback)
4. **Confirmed fallback allowed** — Physical confirm enables LAST as YESTERDAY fallback
5. **Consistent project IDs** — Resolved project must be in PROJECTS allow-list
6. **Context freshness** — Resolution uses latest TIME_SYNC day (host) or local_day (device)

---

## Test Coverage

| Test | Verifies |
|------|----------|
| `test_last` | LAST resolves to most recent |
| `test_yesterday` | YESTERDAY resolves to previous day |
| `test_missing_yesterday_requires_confirmation` | Non-unique yesterday needs confirm |
| `test_all_control_intents_are_typed` | LAST/YESTERDAY in allow-list |
| `test_supported_phrase` | Phrases map correctly |
| `make context-test` | C resolution matches Python |

---

## Failure Modes

| Condition | Host Response | Device Response |
|-----------|---------------|-----------------|
| LAST with empty history | ERR:invalid_project_id | Resolution fails (returns 0) |
| YESTERDAY no unique match | ERR:invalid_project_id | Resolution fails |
| YESTERDAY no match + confirm | Resolves to LAST (fallback) | Resolves to LAST (fallback) |
| Resolved project not in allow-list | ERR:invalid_project_id | N/A (device doesn't validate) |

---

## Acceptance Criteria

- Python phrase patterns documented
- Firmware intent table specified
- Resolution logic for host and firmware
- Confirmation fallback behavior defined
- 6 invariants enumerated
- Test coverage mapped
- Next step (0214) can use this output