# Host Startup and Configuration Specification

**Generated:** 2026-11-18T23:45:00Z
**Git Commit:** b213b2d
**Status:** APPROVED

---

## Contract

**Scope:** Host runtime configuration, project definitions, allow-list, and launcher behavior.

**Purpose:** Define validated configuration and startup diagnostics for the host agent.

---

## Inputs

| Source | Format | Purpose |
|--------|--------|---------|
| `host/config.yaml` | YAML | Host-level settings (projects_root, editor, serial) |
| `host/projects.yaml` | YAML | Project definitions (path, netlist) |
| `host/allowlist.yaml` | YAML | Verb allow-list with risk flags |
| CLI args | argparse | Runtime overrides (--stdio, --port, --baud, --log, --virtual) |

---

## Outputs

- Validated configuration object at startup
- Startup diagnostics logged to audit log
- Running host agent accepting frames

---

## Invariants

1. **Configuration validation** — All YAML files must parse and validate at startup
2. **Path jail** — `projects_root` must be within repository root
3. **Allow-list consistency** — `allowlist.yaml` verbs must match `ALLOWED` in `host_agent.py`
4. **Project consistency** — `projects.yaml` entries must match `PROJECTS` dict in `host_agent.py`
5. **No shell in config** — Editor command must be fixed argv or rejected
6. **Virtual mode explicit** — `--virtual` flag required for simulated operation

---

## Failure Behavior

| Failure | Response |
|---------|----------|
| Config YAML parse error | Exit with error message, no agent started |
| Project path escapes root | Exit with error, path jail violation |
| Allow-list verb mismatch | Exit with error, configuration inconsistency |
| Serial port not found (non-stdio) | Exit with error, suggest --port or --stdio |
| Editor command uses shell | Reject config, require fixed argv |

---

## Configuration Schema

### `host/config.yaml`
```yaml
projects_root: projects          # Relative to repo root, validated
editor: "xdg-open"              # Fixed argv command, NO shell
serial: auto                    # "auto" or specific port path
```

### `host/projects.yaml`
```yaml
projects:
  amplifier: {path: projects/amplifier, netlist: amplifier.cir}
  filter: {path: projects/filter, netlist: filter.cir}
  regulator: {path: projects/regulator, netlist: regulator.cir}
```

### `host/allowlist.yaml`
```yaml
verbs:
  PING: {risky: false}
  OPEN_PROJECT: {risky: false}
  RUN_SIMULATION: {risky: false}
  SHOW_RESULT: {risky: false}
  CLOSE_PROJECT: {risky: true}   # Requires confirm
```

---

## Startup Diagnostics

On successful startup, host agent logs to audit log:
```json
{
  "timestamp": "ISO8601",
  "direction": "host_startup",
  "config": {
    "virtual": true,
    "projects_root": "projects",
    "serial": "auto",
    "project_count": 3,
    "allowlist_verbs": 5
  }
}
```

---

## Launcher Behavior

| Platform | Command | Validation |
|----------|---------|------------|
| Linux | `xdg-open <path>` | `shutil.which("xdg-open")` must exist |
| macOS | `open <path>` | `shutil.which("open")` must exist |
| Windows | `os.startfile(<path>)` | Native, no argv form |

**Invariant:** `shell=True` NEVER used. `close_fds=True` on Linux/macOS.

---

## Acceptance Criteria

- Specification documents all config files, schemas, invariants, failure behavior
- Startup diagnostics defined
- Launcher behavior specified per platform
- Next step (0104) can use this output