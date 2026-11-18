# Virtual Device Transport Specification

**Generated:** 2026-11-19T00:35:00Z
**Git Commit:** b213b2d
**Status:** APPROVED

---

## Contract

**Scope:** Virtual device simulation, serial transport abstraction, and stdio demo for testing without hardware.

**Purpose:** Enable complete host-device loop testing in CI and development without physical ESP32-S3.

---

## Components

### 1. Virtual Device (`host/tools/virtual_device.py`)

Simulates device-side protocol and context.

**Arguments:**
- `--project` (default: "amplifier") — Target project for RUN_SIMULATION
- `--phrase` (default: "open the amplifier project and run the simulation") — Voice phrase to convert to intent

**Flow:**
```python
intent = phrase_to_frame(args.phrase, seq=2)
if args.project != "amplifier" and intent.verb == "RUN_SIMULATION":
    intent = Frame(intent.seq, intent.verb, {**intent.fields, "project": args.project})

session = HostSession(virtual=True)
device = DeviceContext()

# Connection handshake
for frame in session.connect_frames():
    device.handle(frame)
    print(encode(frame).decode().rstrip())

# Request/response loop
for request in (Frame(1, "PING", {}), intent,
                Frame(3, "SHOW_RESULT", {}),
                Frame(4, "RUN_SIMULATION", {"project": args.project}),
                Frame(5, "SHOW_RESULT", {})):
    for response in session.handle(request):
        device.handle(response)
        print(encode(response).decode().rstrip())
```

### 2. Device Context (`firmware/components/context/device_protocol.py`)

Python mirror of firmware context for virtual testing.

**Methods:**
- `handle(frame: Frame)` — Processes TIME_SYNC, PROJECT_EVENT
- `get_last()` — Returns last event for LAST resolution
- `get_yesterday()` — Returns yesterday's event for YESTERDAY resolution

### 3. Serial Transport (`host/transport.py`)

**Functions:**
- `discover_port() -> str | None` — Returns USB CDC port path or None (safe without hardware)
- `serve_serial(port, handler, baud, on_connect)` — Runs serial loop with reconnection

**Reconnection Handshake:**
```python
# On serial connect, immediately send TIME_SYNC
on_connect=lambda: b"".join(encode(frame) for frame in session.connect_frames())
```

### 4. Stdio Demo (`host/tools/stdio_demo.py`)

Exercises host agent in stdio mode (no serial).

**Flow:**
```python
# Feeds frames to host_agent --stdio --virtual
# Verifies: ACK → DONE → ACK → DONE → PROJECT_EVENT → NACK
```

---

## Virtual Device Frame Sequence

| Step | Direction | Frame | Purpose |
|------|-----------|-------|---------|
| 1 | Host→Device | TIME_SYNC (seq=1) | Time sync on connect |
| 2 | Device→Host | ACK (seq=1) | Acknowledge TIME_SYNC |
| 3 | Device→Host | DONE (seq=1) | TIME_SYNC result |
| 4 | Device→Host | PING (seq=1) | Device health check |
| 5 | Host→Device | ACK (seq=1) | Acknowledge PING |
| 6 | Host→Device | DONE (seq=1) | PING result |
| 7 | Device→Host | Intent (seq=2) | e.g., RUN_SIMULATION |
| 8 | Host→Device | ACK (seq=2) | Acknowledge intent |
| 9 | Host→Device | DONE (seq=2) | Simulation result |
| 10 | Host→Device | PROJECT_EVENT (seq=2) | Context update |
| 11 | Device→Host | SHOW_RESULT (seq=3) | Request result |
| 12 | Host→Device | ACK (seq=3) | Acknowledge |
| 13 | Host→Device | DONE (seq=3) | Cached result |
| 14 | Device→Host | RUN_SIMULATION (seq=4) | Repeat simulation |
| 15 | Host→Device | ACK (seq=4) | Acknowledge |
| 16 | Host→Device | DONE (seq=4) | Simulation result |
| 17 | Host→Device | PROJECT_EVENT (seq=4) | Context update |
| 18 | Device→Host | SHOW_RESULT (seq=5) | Request result |
| 19 | Host→Device | ACK (seq=5) | Acknowledge |
| 20 | Host→Device | DONE (seq=5) | Cached result |

---

## Invariants

1. **No hardware required** — Virtual device runs entirely in Python
2. **Protocol fidelity** — Uses same `encode`/`decode` as real transport
3. **Context mirror** — `DeviceContext` mirrors firmware `context.c` behavior
4. **Session consistency** — Uses real `HostSession` and `dispatch`
4. **Deterministic** — Same phrase → same frame sequence
5. **CI safe** — `discover_port()` returns None, no serial dependency
6. **Reconnection tested** — `serve_serial` handshake verified in tests

---

## Test Coverage

| Test | Verifies |
|------|----------|
| `test_session_sync_and_event_update_device_context` | TIME_SYNC + PROJECT_EVENT update DeviceContext |
| `test_discovery_is_safe_without_serial_dependency` | `discover_port()` returns None, no crash |
| `test_serial_unplug_reconnects_and_repeats_handshake` | Reconnection sends TIME_SYNC |

---

## Acceptance Criteria

- Virtual device frame sequence documented
- Device context mirror specified
- Serial transport abstraction defined
- Stdio demo purpose clear
- 6 invariants enumerated
- Test coverage mapped
- Next step (0154) can use this output