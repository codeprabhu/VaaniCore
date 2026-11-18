# Demo Scope Specification

**Generated:** 2026-11-18T22:40:00Z
**Git Commit:** a407329
**Status:** SIGNED OFF (this document constitutes the signed-off narrow demo scenario)

---

## Supported Voice Command

**Primary:** "open the amplifier project and run the simulation"
**Variants (all map to same intent):**
- "run simulation on amplifier"
- "amplifier run simulation"
- "open amplifier and run simulation"

**Intent Frame:** `Frame(seq=N, "RUN_SIMULATION", {"project": "amplifier", "open": "1"})`

---

## Host Actions (Allow-Listed Only)

| Step | Action | Implementation | Safety |
|------|--------|----------------|--------|
| 1 | Open project directory | `host/launcher.py:launch_project()` → `xdg-open projects/amplifier` (Linux) | Fixed argv, no shell, path jailed to `projects/amplifier` |
| 2 | Run SPICE simulation | `host/host_agent.py:dispatch()` → `subprocess.run(["ngspice", "-b", "-o", "results.log", "amplifier.cir"])` | Runs in project dir only, no shell, ngspice must exist |
| 3 | Parse measurements | `host/measurements.py:parse_meas()` reads `results.log` | Only accepts numeric `.meas` lines |

---

## Response (Virtual Mode)

```json
{
  "status": "ok",
  "project": "amplifier",
  "gain_db": "TARGET",
  "bw_hz": "TARGET",
  "label": "SIMULATED",
  "opened": "1"
}
```

**Response (Real Mode, requires ngspice):**
```json
{
  "status": "ok",
  "project": "amplifier",
  "gain_db": "<measured>",
  "bw_hz": "<measured>",
  "label": "MEASURED"
}
```

---

## Context Updates

- `HostSession.last_result` cached for `SHOW_RESULT`
- `PROJECT_EVENT` emitted: `action=RUN_SIMULATION, project=amplifier, epoch=<unix>`
- Device context updated via `PROJECT_EVENT` frame (LAST → amplifier)

---

## Fallback / Error Cases

| Condition | Response | Requires Confirm |
|-----------|----------|------------------|
| Unknown project ID | `ERR: code=invalid_project_id` | No |
| Netlist missing | `ERR: code=netlist_missing` | No |
| ngspice not installed (real mode) | `ERR: code=ngspice_unavailable` | No |
| Simulation fails (non-zero exit) | `ERR: code=simulation_failed` | No |
| Opener unavailable (xdg-open missing) | `ERR: code=opener_unavailable` | No |
| CLOSE_PROJECT | `ERR: code=physical_confirm_required` | Yes |

---

## Out of Scope for Demo

- Filter/regulator projects (available but not in primary demo)
- LAST/YESTERDAY context chaining (tested separately)
- Wake word / VAD (PTT is Day-14 path)
- Real audio capture (hardware blocked)
- Real ML inference (dataset blocked)
- OLED display (driver absent)
- Hardware measurements (P1/P2/P3 blocked)

---

## Acceptance Criteria

- Single voice command opens known project and runs safe simulation
- All actions allow-listed and path-jailed
- Virtual mode works without hardware/ngspice
- Real mode fails closed without ngspice
- Response labels SIMULATED vs MEASURED correctly
- Context persists for SHOW_RESULT
- Specification signed off and stored as `docs/DEMO_SCOPE_SPEC.md`