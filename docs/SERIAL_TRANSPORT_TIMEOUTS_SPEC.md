# Serial Transport and Timeouts Specification

**Generated:** 2026-11-19T02:35:00Z
**Git Commit:** afb3795
**Status:** APPROVED

---

## Contract

**Scope:** USB CDC serial transport, port discovery, timeouts, and reconnection behavior.

**Purpose:** Define reliable serial communication between ESP32-S3 and Linux host.

---

## Port Discovery (`host/transport.py:discover_port`)

```python
def discover_port() -> str | None:
    """Find VaaniCore USB CDC port by Vid/Pid."""
    for port in serial.tools.list_ports.comports():
        if port.vid == 0x303A and port.pid == 0x1001:  # Espressif defaults
            return port.device
    return None
```
- Searches `/dev/ttyUSB*`, `/dev/ttyACM*`
- Matches Espressif USB Vid/Pid (0x303A / 0x1001)
- Returns `None` if not found (safe in CI)

---

## Serial Serve (`host/transport.py:serve_serial`)

```python
def serve_serial(
    port: str,
    handler: Callable[[bytes], bytes],
    baud: int = 115200,
    on_connect: Callable[[], bytes] | None = None
) -> None:
    """Run serial read/write loop with reconnection handshake."""
    ser = serial.Serial(port, baud, timeout=1.0)
    try:
        if on_connect:
            ser.write(on_connect())  # Sends TIME_SYNC immediately
        while True:
            line = ser.readline()
            if not line:
                continue  # Timeout, loop continues
            response = handler(line)
            if response:
                ser.write(response)
    finally:
        ser.close()
```

### Parameters
| Parameter | Default | Description |
|-----------|---------|-------------|
| `port` | Required | Serial device path |
| `handler` | Required | Function: bytes request → bytes response |
| `baud` | 115200 | Baud rate |
| `on_connect` | None | Callback fired on connect, returns bytes to send |

---

## Timeouts

| Timeout | Value | Location | Purpose |
|---------|-------|----------|---------|
| Serial read | 1.0s | `serve_serial()` `serial.Serial(timeout=1.0)` | Prevents blocking on readline |
| RETRY_DELAY | 0.3s | `reliability.py` | Device retry interval |
| MAX_ATTEMPTS | 3 | `reliability.py` | Device max retries |
| TASK_TIMEOUT | 30s | `reliability.py` | Max task duration (not enforced) |
| IDLE_TIMEOUT | 300s | `reliability.py` | Idle detection (planned) |

---

## Reconnection Behavior

### Current Implementation
- `serve_serial()` runs until serial exception or process exit
- On disconnect: `serve_serial()` returns (closes port)
- **No automatic reconnection** in current code
- Host agent process must be restarted (systemd/service manager)

### Reconnection Handshake (on restart)
```python
# host_agent.py main()
on_connect = lambda: b"".join(encode(frame) for frame in session.connect_frames())
serve_serial(port, handler, baud, on_connect=on_connect)
```
- `session.connect_frames()` returns `[TIME_SYNC]`
- Sent immediately on serial open
- Device responds with ACK + DONE

### Device-Side Reconnection
- ESP32-S3 USB CDC: hardware handles physical reconnection
- TinyUSB stack re-enumerates on host reconnect
- Device firmware: no special reconnection logic needed
- On receiving TIME_SYNC: updates clock, sends ACK

---

## Invariants

1. **Safe discovery** — `discover_port()` returns None, never crashes
2. **TIME_SYNC on connect** — `on_connect` fires immediately
3. **Read timeout** — 1s prevents indefinite block
4. **Handler isolation** — `handler()` exceptions caught in host_agent
5. **Clean close** — `finally: ser.close()` on exit
6. **Baud rate fixed** — 115200 (USB CDC ignores but kept for compatibility)

---

## Test Coverage

| Test | Verifies |
|------|----------|
| `test_discovery_is_safe_without_serial_dependency` | `discover_port()` returns None safely |
| `test_serial_unplug_reconnects_and_repeats_handshake` | Reconnection sends TIME_SYNC |

---

## Failure Modes

| Condition | Behavior |
|-----------|----------|
| No VaaniCore device | `discover_port()` returns None → host exits with error |
| Port permission denied | `serial.Serial()` raises → host exits with error |
| Device disconnects mid-session | `readline()` returns empty → loop continues → eventually serial exception → `serve_serial()` exits |
| Host process killed | Port closed by OS, device USB stack resets |
| Baud rate mismatch | USB CDC ignores baud, communication works |

---

## Acceptance Criteria

- Port discovery algorithm specified
- serve_serial() loop with timeouts documented
- Reconnection handshake (TIME_SYNC on connect) defined
- Timeout table complete
- 6 invariants enumerated
- Test coverage mapped
- Next step (0274) can use this output