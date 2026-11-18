# Repository Inventory Specification

## Contract

**Scope:** Tracked files, ignored files, branches, tags, and working-tree changes in the VaaniCore repository.

**Purpose:** Establish a truthful, reproducible baseline before modifying the existing VaaniCore implementation.

## Inputs

- Git repository at `/home/shrivathssp/Desktop/vaanicore`
- Working tree state
- Remote origin configuration

## Outputs

- Inventory report documenting:
  - All tracked files by category (source, test, config, documentation, results)
  - `.gitignore` patterns and their rationale
  - Branch structure (local and remote)
  - Tag history
  - Untracked/working-tree changes
  - File hashes for key artifacts

## Invariants

1. **No data loss:** Inventory must not discard or overwrite existing user changes
2. **Completeness:** All tracked files must be accounted for
3. **Accuracy:** File categories must reflect actual content, not assumptions
4. **Reproducibility:** Same commands must produce same results

## Failure Behavior

- If git commands fail → record error and mark step BLOCKED
- If working tree has uncommitted changes not in .gitignore → document them explicitly
- If remote is unreachable → note as limitation, continue with local data

## Key File Categories

### Source Code
- **Host (Python):** `host/` - protocol, session, dispatcher, launcher, transport, intent NLU, audit log, reliability
- **Firmware (C):** `firmware/` - main, protocol component, DSP component, context component
- **ML (Python):** `ml/` - features, model, dataset, training, export, evaluation
- **Hardware (Python):** `hardware/` - pinmap validation, power budget, CAD
- **Tools (Python):** `tools/` - audit, FMEA validation, dataset recording, provenance
- **Bench (Python):** `bench/` - benchmarks, analysis, timing study
- **Deck (Python):** `deck/` - presentation generation

### Configuration
- `host/config.yaml` - host runtime configuration
- `host/projects.yaml` - project definitions
- `host/allowlist.yaml` - action allow-list
- `firmware/sdkconfig.defaults` - ESP-IDF defaults
- `ml/configs/default.json` - ML training config
- `ml/configs/classes.json` - intent class definitions

### Tests
- Unit tests: `tests/test_*.py` (26 test modules)
- C test vectors: `tests/protocol/vectors.json`
- C test drivers: `tests/*_c.c`

### Documentation
- Root: `README.md`, `PROMPT.md`, `TODO_HUMAN.md`, `workflow.md`
- `docs/` - specifications, walkthroughs, decisions, status matrices
- `firmware/README.md`, `hardware/kicad/README.md`

### Results/Evidence
- `results/` - benchmark outputs, audit logs, validation artifacts
- `deck/out/` - generated presentation artifacts

### Projects
- `projects/amplifier/`, `projects/filter/`, `projects/regulator/` - KiCad projects and SPICE netlists

## Acceptance Criteria

- Inventory report exists and is accurate
- All 50 unit tests still pass after inventory
- WORKFLOW_STATUS.md updated with trace evidence
- Next step (0003) can use this output