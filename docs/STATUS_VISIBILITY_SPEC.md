# Status Visibility Specification

**Generated:** 2026-11-19T05:15:00Z
**Git Commit:** d6536ed
**Status:** APPROVED

---

## Contract

**Scope:** User-visible status indicators (device LEDs, host logs, demo output) for VaaniCore prototype.

**Purpose:** Define how operators observe system state without web dashboard.

---

## Device Status (LEDs)

| LED | GPIO | Pattern | Meaning |
|-----|------|---------|---------|
| LISTEN | 18 | Blink 1Hz | Idle, waiting for PTT |
| LISTEN | 18 | Solid | Capturing audio (PTT held) |
| BUSY | 21 | Solid | Processing (DSP/ML/comms) |
| ERR | 47 | Blink 5Hz | Error (CRC, comms, hardware) |
| ERR | 47 | Solid | Fatal error |

**Implementation:** `firmware/main/ui.c` → `vc_ui_set_led_pattern()`

---

## Host Status (Audit Log)

### Log File: `logs/host_agent.jsonl`

**Format (JSONL):**
```json
{"timestamp": "2026-11-19T05:15:00.123456+00:00", "direction": "device_to_host", "frame": {"seq": 1, "verb": "PING", "fields": {}}}
{"timestamp": "2026-11-19T05:15:00.123567+00:00", "direction": "host_to_device", "frame": {"seq": 1, "verb": "ACK", "fields": {"seq": "1"}}}
{"timestamp": "2026-11-19T05:15:00.123678+00:00", "direction": "host_to_device", "frame": {"seq": 1, "verb": "DONE", "fields": {"status": "ok"}}}
```

### Logged Events
- Every valid request (device_to_host)
- Every response (host_to_device)
- Protocol errors (host_to_device with NACK)
- Host internal errors (host_error)

---

## Host Status (Result Cache)

### `HostSession.last_result`
- Updated on RUN_SIMULATION success
- Contains: status, project, gain_db, bw_hz, label
- Returned by SHOW_RESULT verb
- Lifetime: session duration

---

## Demo Visibility (`host/tools/stdio_demo.py`)

Prints frame sequence to stdout:
```
@1:TIME_SYNC:epoch=...,tz_offset_min=...CRC
@1:ACK:seq=1CRC
@1:DONE:status=okCRC
@2:RUN_SIMULATION:project=amplifier,open=1CRC
@2:ACK:seq=2CRC
@2:DONE:bw_hz=TARGET,gain_db=TARGET,label=SIMULATED,opened=1,project=amplifier,status=okCRC
@2:PROJECT_EVENT:action=RUN_SIMULATION,project=amplifier,epoch=...CRC
```

---

## Invariants

1. **No web dashboard** — Offline-first, status via LEDs + logs
2. **LEDs unambiguous** — Listen/busy/err patterns distinct
3. **Audit log complete** — Every frame logged with metadata
4. **No audio in logs** — Privacy preserved
5. **Result cache accessible** — SHOW_RESULT returns last success
6. **Demo output readable** — Frame sequence printed for debugging

---

## Test Coverage

| Test | Verifies |
|------|----------|
| `make sim-demo` | Frame sequence printed |
| `test_jsonl_has_frame_metadata_and_no_audio_field` | Audit log structure |

---

## Failure Modes

| Condition | Visibility |
|-----------|------------|
| Device firmware crash | ERR LED solid, no frames |
| Host audit log full | Disk full error, host exits |
| LED GPIO failure | Pattern not visible |
| Result cache lost | SHOW_RESULT returns ERR |

---

## Acceptance Criteria

- LED patterns specified for all states
- Audit log format defined
- Result cache behavior documented
- Demo output format shown
- 6 invariants enumerated
- Next step (0494) can use this output