# Hardware Source Intake Specification

**Generated:** 2026-11-18T22:50:00Z
**Git Commit:** a407329

---

## Contract

**Scope:** Separate Raphael PCB archive, VaaniCore hardware directory, and native KiCad artifacts.

**Purpose:** Establish source provenance and merge decision for hardware design.

## Inputs

- Raphael KiCad archive (separate upload, not yet in repo): `.kicad_pro`, `.kicad_sch`, `.kicad_pcb`
- VaaniCore `hardware/pinmap.csv` (authoritative netlist-level source)
- VaaniCore `firmware/main/pins.h` (firmware pin definitions)
- VaaniCore `hardware/kicad/` directory (README, drc_checklist.md, netlist_spec.csv)
- Existing project KiCad files (amplifier, filter, regulator) — SPICE projects, not main board

## Outputs

- Provenance record: archive source, file hashes, KiCad version compatibility
- Merge decision: adopt/adapt/reject Raphael design
- Reconciliation report: pin map conflicts, schematic differences, DRC status

## Invariants

1. **Preserve originals:** Never overwrite native KiCad source files; work on copies
2. **Pin map consistency:** All pin assignments must match across CSV, C header, KiCad
3. **Block on conflict:** Raise blocking issue when pin assignments disagree; do not silently choose
4. **Provenance tracking:** Record all copies, modifications, and decisions

## Failure Behavior

- If Raphael archive unavailable → mark BLOCKED, continue independent work
- If pin conflicts found → document each conflict, do not proceed to fabrication
- If KiCad version incompatible → note version, assess migration effort

## Current State

| Source | Status | Location |
|--------|--------|----------|
| Raphael archive | NOT IN REPO | Separate upload (path unknown) |
| VaaniCore pinmap.csv | AUTHORITATIVE | `hardware/pinmap.csv` (13 pins) |
| Firmware pins.h | CONSISTENT | `firmware/main/pins.h` (matches + UART/JTAG) |
| KiCad project (main board) | NOT STARTED | `hardware/kicad/` has only docs |
| SPICE project KiCad | EXISTING | `projects/*/*.kicad_pro` (different purpose) |

## Acceptance Criteria

- Raphael archive located and hashed
- Pin map reconciliation complete (match or documented conflicts)
- Merge decision recorded
- Next step (0054) can use this output