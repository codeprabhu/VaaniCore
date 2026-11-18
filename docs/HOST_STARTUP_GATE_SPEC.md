# Host Startup Gate Specification

**Generated:** 2026-11-19T00:55:00Z
**Git Commit:** b213b2d
**Status:** APPROVED

---

## Contract

**Scope:** Host agent startup validation, transport establishment, and readiness criteria.

**Purpose:** Define deterministic startup sequence that must succeed before host accepts device frames.

---

## Startup Sequence

### 1. Argument Parsing & Validation
```python
parser.add_argument("--stdio", action="store_true")
parser.add_argument("--port", help="USB serial port")
parser.add_argument("--baud", type=int, default=115200)
parser.add_argument("--log", default="logs/host_agent.jsonl")
parser.add_argument("--virtual", action="store_true")
```

**Validation:**
- Exactly one of `--stdio` or `--port` (or auto-discovery) required
- `--port` ignored if `--stdio` set
- `--baud` positive integer
- `--log` directory created if missing

### 2. Configuration Loading
- `host/config.yaml` parsed (projects_root, editor, serial)
- `host/projects.yaml` parsed → PROJECTS dict
- `host/allowlist.yaml` parsed → ALLOWED/RISKY verbs
- Validation: paths within root, verbs consistent

### 3. Session Creation
```python
session = HostSession(virtual=args.virtual)
```
- `next_seq = 1`
- `last_result = None`
- `virtual` flag stored for dispatch

### 4. Transport Establishment

#### Stdio Mode (`--stdio`)
- No port discovery
- Reads `sys.stdin.buffer` line by line
- Writes responses to `sys.stdout.buffer`
- No TIME_SYNC sent automatically (test controls it)

#### Serial Mode (default)
```python
port = args.port or discover_port()
if not port:
    raise SystemExit("no VaaniCore serial port found; provide --port or use --stdio")
serve_serial(port, handler, baud, on_connect=lambda: encode(TIME_SYNC))
```

- `discover_port()`: searches `/dev/ttyUSB*`, `/dev/ttyACM*` for Vid/Pid match
- Returns `None` if no port found (safe in CI)
- `serve_serial()`: opens pyserial, sets timeout, runs read loop

### 5. Connection Handshake (Serial Only)
- `on_connect` callback fires **immediately** on serial open
- Sends `TIME_SYNC` frame (seq=1) before any device frames
- Device responds with ACK + DONE
- Host session now ready for requests

---

## Gate Criteria (All Must Pass)

| Criterion | Check | Failure Action |
|-----------|-------|----------------|
| Config valid | YAML parse, path jail, verb consistency | Exit with error |
| Transport ready | Port found (serial) or stdio available | Exit with error |
| Session created | HostSession instantiated | Exception |
| TIME_SYNC sent (serial) | on_connect callback fires | Log warning, continue |
| Audit log writable | logs/ directory created, file opened | Exit with error |

---

## Failure Modes

| Failure | Response |
|---------|----------|
| Config YAML syntax error | Print error, exit 1 |
| projects_root escapes repo root | Print error, exit 1 |
| allowlist.yaml missing verb | Print error, exit 1 |
| No serial port (non-stdio) | Print error, exit 1 |
| Serial port permission denied | Print error, exit 1 |
| Audit log directory not writable | Print error, exit 1 |
| pyserial not installed | ImportError, exit 1 |

---

## Invariants

1. **Explicit transport** — Must choose stdio or serial, no implicit default
2. **TIME_SYNC first (serial)** — No device frames processed before TIME_SYNC
3. **Config validation at startup** — Fail fast, no deferred errors
4. **Audit log ready** — Directory created, file opened before first frame
5. **Virtual mode explicit** — `--virtual` flag required for SIMULATED behavior
6. **Clean shutdown** — Ctrl-C / EOF closes serial, flushes logs

---

## Test Coverage

| Test | Verifies |
|------|----------|
| `test_module_exists_and_help_contract_is_documented` | Module loads, --help works |
| `test_discovery_is_safe_without_serial_dependency` | discover_port() returns None safely |
| `test_serial_unplug_reconnects_and_repeats_handshake` | Reconnection sends TIME_SYNC |
| `make sim-demo` | Stdio mode full loop works |

---

## Acceptance Criteria

- Startup sequence documented step by step
- Gate criteria table complete
- Failure modes enumerated
- 6 invariants listed
- Test coverage mapped
- Next step (0174) can use this output