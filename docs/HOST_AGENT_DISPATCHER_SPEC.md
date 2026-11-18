# Host Agent Dispatcher Specification

**Generated:** 2026-11-18T23:55:00Z
**Git Commit:** b213b2d
**Status:** APPROVED

---

## Contract

**Scope:** Allow-listed action dispatcher for VaaniCore host agent.

**Purpose:** Define complete dispatcher behavior, invariants, and failure modes.

---

## Inputs

- `Frame` from `host/protocol.py` (seq, verb, fields)
- `confirm: bool` — explicit confirmation for risky actions
- `virtual: bool` — simulation mode flag

---

## Outputs

- `Frame` response (ACK always sent by session, then DONE/ERR)
- Side effects: project launch, ngspice subprocess, audit log entries

---

## Verb Specifications

### PING
```python
# Request: Frame(seq, "PING", {})
# Response: Frame(seq, "DONE", {"status": "ok"})
```
- Always allowed, no side effects
- Health check / connectivity test

---

### OPEN_PROJECT
```python
# Request: Frame(seq, "OPEN_PROJECT", {"project": "amplifier"})
# Response (virtual): Frame(seq, "DONE", {"status": "ok", "project": "amplifier", "opener": "xdg-open", "label": "SIMULATED"})
# Response (real): Frame(seq, "DONE", {"status": "ok", "project": "amplifier", "opener": "xdg-open", "label": "MEASURED"})
```
- Validates project ID via `_project()`
- Calls `launch_project(project, dry_run=virtual)`
- Returns opener command used
- Emits PROJECT_EVENT on success

---

### RUN_SIMULATION
```python
# Request: Frame(seq, "RUN_SIMULATION", {"project": "amplifier", "open": "1"})
# Response (virtual): Frame(seq, "DONE", {"status": "ok", "project": "amplifier", "gain_db": "TARGET", "bw_hz": "TARGET", "label": "SIMULATED", "opened": "1"})
# Response (real, success): Frame(seq, "DONE", {"status": "ok", "project": "amplifier", "gain_db": "20.5", "bw_hz": "1000000", "label": "MEASURED"})
# Response (real, ngspice missing): Frame(seq, "ERR", {"code": "ngspice_unavailable"})
# Response (real, sim failed): Frame(seq, "ERR", {"code": "simulation_failed"})
```
- Validates project ID via `_project()`
- Checks netlist exists: `project/{project}.cir`
- If `open=1`: calls `launch_project(project, dry_run=virtual)` first
- **Virtual mode**: Returns SIMULATED with TARGET values, no ngspice
- **Real mode**: Requires ngspice in PATH, runs `ngspice -b -o results.log netlist.cir` in project dir
- Parses measurements via `host/measurements.py:parse_meas()`
- Caches result in `HostSession.last_result` for SHOW_RESULT
- Emits PROJECT_EVENT on success

---

### SHOW_RESULT
```python
# Request: Frame(seq, "SHOW_RESULT", {})
# Response (has result): Frame(seq, "DONE", {"status": "ok", "project": "amplifier", "gain_db": "...", "bw_hz": "...", "label": "..."})
# Response (no result): Frame(seq, "ERR", {"code": "no_result_available"})
```
- Returns cached `HostSession.last_result`
- No side effects
- Does not emit PROJECT_EVENT

---

### CLOSE_PROJECT
```python
# Request: Frame(seq, "CLOSE_PROJECT", {"project": "LAST"})
# Response (confirmed): Frame(seq, "DONE", {"status": "ok"})
# Response (not confirmed): Frame(seq, "ERR", {"code": "physical_confirm_required"})
```
- **Risky verb** — requires `confirm=True`
- Resolves project via `_project()` (supports LAST/YESTERDAY via context)
- No actual close action (placeholder for future)
- Emits PROJECT_EVENT on success

---

## Helper Functions

### `_project(name: str) -> pathlib.Path`
```python
# Validates:
# 1. name in PROJECTS dict (from projects.yaml)
# 2. pathlib.Path(name).name == name (no path traversal)
# 3. path.resolve() has ROOT in parents (path jail)
# Raises ValueError on any failure
```

### `launch_project(project: Path, dry_run: bool) -> str`
```python
# Platform-specific fixed-argv launcher:
# Linux:   ["xdg-open", str(project)] if shutil.which("xdg-open")
# macOS:   ["open", str(project)] if shutil.which("open")
# Windows: os.startfile(str(project)) (no argv form)
# Returns opener name (e.g., "xdg-open") or raises RuntimeError
```

### `parse_meas(log_text: str) -> dict`
```python
# Parses ngspice .meas output lines:
# .meas gain_db ... 20.5
# .meas bw_hz ... 1000000
# Returns {"gain_db": "20.5", "bw_hz": "1000000"}
# Only accepts numeric values (regex validation)
```

---

## Invariants

1. **Allow-list only** — Unknown verbs → ERR:verb_not_allowed
2. **Path jail** — Project resolution validates `ROOT in path.parents`
3. **No shell** — Launcher uses fixed argv, `shell=True` forbidden
4. **Confirm for risky** — CLOSE_PROJECT requires `confirm=True`
5. **Virtual explicit** — `virtual=True` returns SIMULATED/TARGET, never MEASURED
6. **Fails closed** — Real mode without ngspice → ERR:ngspice_unavailable
7. **Measurement bounded** — Parser only accepts numeric .meas lines
8. **Result caching** — Only RUN_SIMULATION success caches for SHOW_RESULT

---

## Failure Modes

| Condition | Response | Code |
|-----------|----------|------|
| Verb not in ALLOWED | ERR | verb_not_allowed |
| Risky verb without confirm | ERR | physical_confirm_required |
| Unknown project ID | ERR | invalid_project_id |
| Netlist file missing | ERR | netlist_missing |
| Launcher unavailable | ERR | opener_unavailable |
| ngspice not in PATH | ERR | ngspice_unavailable |
| ngspice exit code != 0 | ERR | simulation_failed |
| No cached result for SHOW_RESULT | ERR | no_result_available |

---

## Acceptance Criteria

- All 5 verbs specified with request/response formats
- Helper functions defined with validation logic
- Invariants enumerated (8)
- Failure modes table complete
- Next step (0114) can use this output