# Launcher and Allow-List Specification

**Generated:** 2026-11-19T00:15:00Z
**Git Commit:** b213b2d
**Status:** APPROVED

---

## Contract

**Scope:** Platform-specific project launcher and verb allow-list with risk classification.

**Purpose:** Define safe, auditable action execution without shell access.

---

## Allow-List (Verbs)

Defined in `host/allowlist.yaml` and mirrored in `host/host_agent.py`:

| Verb | Risky | Description |
|------|-------|-------------|
| PING | false | Connectivity test |
| OPEN_PROJECT | false | Open project directory in file manager |
| RUN_SIMULATION | false | Run SPICE simulation (optionally open project first) |
| SHOW_RESULT | false | Retrieve last simulation result |
| CLOSE_PROJECT | true | Close project (placeholder, requires confirm) |

**Invariant:** `ALLOWED` set in `host_agent.py` must match `allowlist.yaml` verbs exactly.

---

## Launcher Behavior

### `open_command(project: Path, platform_name: str) -> list[str] | None`
Returns fixed argv for platform, or None if unavailable.

| Platform | Command | Condition |
|----------|---------|-----------|
| Linux | `["xdg-open", str(project)]` | `shutil.which("xdg-open")` |
| macOS | `["open", str(project)]` | `shutil.which("open")` |
| Windows | `None` (uses `os.startfile`) | Always available |

### `launch_project(project: Path, dry_run: bool) -> str`
Executes or simulates project launch.

```python
command = open_command(project)
if sys.platform.startswith("win"):
    if dry_run: return "os.startfile"
    os.startfile(str(project.resolve()))
    return "os.startfile"
if not command:
    raise RuntimeError("platform opener unavailable")
if dry_run:
    return " ".join(command)  # e.g., "xdg-open /path/to/project"
subprocess.Popen(command, cwd=project, close_fds=True)
return command[0]  # e.g., "xdg-open"
```

---

## Invariants

1. **No shell execution** — `shell=True` never used; fixed argv only
2. **Path jail** — Project path validated in `_project()` before launch
3. **Opener validation** — `shutil.which()` checks availability before use
4. **Close file descriptors** — `close_fds=True` on Linux/macOS subprocess
5. **Working directory** — Subprocess runs in project directory (`cwd=project`)
6. **Dry-run support** — `virtual=True` in dispatch passes `dry_run=True` to launcher
7. **Allow-list gate** — Dispatcher checks `verb in ALLOWED` before any launcher call
8. **Risky confirm gate** — `CLOSE_PROJECT` requires `confirm=True` in dispatch

---

## Failure Modes

| Condition | Response | Code |
|-----------|----------|------|
| Verb not in ALLOWED | ERR | verb_not_allowed |
| Risky verb without confirm | ERR | physical_confirm_required |
| Unknown project ID | ERR | invalid_project_id |
| Platform opener unavailable | ERR | opener_unavailable |
| Project path escapes root | ERR (in _project) | invalid_project_id |

---

## Test Coverage

| Test | Verifies |
|------|----------|
| `test_linux_command_is_fixed_argv` | Linux returns `["xdg-open", path]` |
| `test_windows_uses_startfile_path` | Windows uses `os.startfile` |
| `test_host_source_forbids_shell_true` | No `shell=True` in host_agent.py |
| `test_path_is_project_id_only` | Path jail enforced |
| `test_risky_action_requires_confirm` | CLOSE_PROJECT needs confirm |
| `test_unknown_verb_rejected` | Allow-list enforced |
| `test_virtual_run_can_explicitly_open_project_first` | open=1 works in virtual mode |

---

## Acceptance Criteria

- Allow-list defined with risk flags
- Launcher specified per platform with fixed argv
- 8 invariants enumerated
- Failure modes table complete
- Test coverage mapped
- Next step (0134) can use this output