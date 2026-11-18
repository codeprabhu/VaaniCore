# Audit Log and Confirmation Specification

**Generated:** 2026-11-19T00:25:00Z
**Git Commit:** b213b2d
**Status:** APPROVED

---

## Contract

**Scope:** JSONL audit logging for all host-device communication and confirmation policy for risky actions.

**Purpose:** Provide tamper-evident, inspectable log of all protocol interactions without sensitive data.

---

## Audit Log Format (JSONL)

Each line is a complete JSON object:

```json
{
  "timestamp": "2026-11-18T23:59:59.123456+00:00",
  "direction": "device_to_host | host_to_device | host_error",
  "frame": {
    "seq": 1,
    "verb": "PING",
    "fields": {}
  },
  "error": "optional error description"
}
```

### Field Definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| timestamp | string (ISO8601) | Yes | UTC timestamp with microseconds |
| direction | string | Yes | One of: `device_to_host`, `host_to_device`, `host_error` |
| frame | object | Yes | Decoded frame: seq (int), verb (string), fields (dict) |
| error | string | No | Error description for failed decodes or host errors |

---

## Logged Events

| Event | Direction | Frame Verb | Notes |
|-------|-----------|------------|-------|
| Valid request received | device_to_host | Any | After successful decode |
| Response sent | host_to_device | ACK, DONE, ERR, NACK, PROJECT_EVENT | After dispatch |
| Decode error (CRC/malformed) | host_to_device | NACK | Includes error in `error` field |
| Host internal error | host_error | ERR | Unexpected exception, includes error |

---

## Confirmation Policy

### Risky Verbs
```python
RISKY = {"CLOSE_PROJECT"}
```

### Dispatch Check
```python
if frame.verb in RISKY and not confirm:
    return Frame(frame.seq, "ERR", {"code": "physical_confirm_required"})
```

### Confirmation Sources
- **Physical button** — Device sends CONFIRM frame (GPIO15 press)
- **Virtual mode** — Test/cli passes `confirm=True` to dispatch
- **Future: Voice** — "confirm"/"yes"/"do it" → CONFIRM frame

### Confirmation Flow
1. Host receives risky verb (CLOSE_PROJECT) without confirm
2. Host returns ERR:physical_confirm_required
3. Device/UI prompts user for physical confirmation
4. User presses confirm button → device sends CONFIRM frame
5. Host receives CONFIRM → next risky request includes `confirm=True`
6. Host executes action, returns DONE

---

## Invariants

1. **No audio in logs** — Audio samples, MFCC features, raw I2S data never logged
2. **Append-only** — Log file opened in append mode (`"a"`), never truncated
3. **Structured JSON** — Every line valid JSON, parseable independently
4. **Frame metadata complete** — Seq, verb, fields always present
5. **Error context preserved** — Decode errors include error string for debugging
6. **Timestamps UTC** — All timestamps in UTC with timezone offset
7. **Confirm required for risky** — CLOSE_PROJECT never executes without confirm
8. **NACK logged** — Protocol errors logged with recovered sequence

---

## Failure Modes

| Condition | Behavior |
|-----------|----------|
| Log directory missing | Created automatically (`logs/`) |
| Log file permission error | Exception raised, host fails to start |
| Disk full | Exception raised, host fails |
| Malformed frame decode | NACK sent, logged with error, sequence recovered if possible |
| Host exception | ERR sent, logged as host_error with exception type |

---

## Test Coverage

| Test | Verifies |
|------|----------|
| `test_jsonl_has_frame_metadata_and_no_audio_field` | JSONL structure, no audio fields |
| `test_risky_action_requires_confirm` | CLOSE_PROJECT needs confirm |

---

## Acceptance Criteria

- JSONL format specified with all fields
- Logged events table complete
- Confirmation policy defined for risky verbs
- 8 invariants enumerated
- Failure modes documented
- Test coverage mapped
- Next step (0144) can use this output