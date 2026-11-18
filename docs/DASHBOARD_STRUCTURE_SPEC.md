# Dashboard Structure Specification

**Generated:** 2026-11-19T05:05:00Z
**Git Commit:** d6536ed
**Status:** APPROVED

---

## Contract

**Scope:** Presentation deck (dashboard) structure and evidence integration for VaaniCore demo.

**Purpose:** Define how evidence is presented in the submission deck.

---

## Deck Structure (`deck/build_deck.py`)

### Template
- **Source:** `inputs/Vishwakarma_Awards_2026-27_Stage_2_Submission_Template.pptx`
- **Method:** lxml OOXML direct manipulation (python-pptx unavailable)
- **Output:** `deck/out/Vishwakarma_Stage2_VaaniCore.pptx`

### Slide Map (18 Slides)
| Slide | Title | Content Source |
|-------|-------|----------------|
| 1 | Title | Template |
| 2 | Problem Statement | Template + `docs/idea_scope.md` |
| 3 | Solution Overview | Template + architecture diagram |
| 4 | Architecture | `deck/assets/architecture.svg` |
| 5 | Protocol & Reliability | `docs/protocol.md`, `docs/ARCHITECTURE_BOUNDARY_TABLE.md` |
| 6 | Audio Pipeline | `docs/dsp_spec.md`, `docs/I2S_GDMA_AUDIO_CAPTURE_SPEC.md` |
| 7 | ML Pipeline | `docs/DS_CNN_TRAINING_PIPELINE_SPEC.md` |
| 8 | Security Model | `docs/SECURITY_INVARIANTS_CHECKLIST.md` |
| 9 | Context & Continuity | `docs/CONTEXT_STORE_PYTHON_SPEC.md`, `docs/CONTEXT_STORE_C_SPEC.md` |
| 10 | Hardware Design | `docs/PINMAP_RECONCILIATION_SPEC.md` (blocked) |
| 11 | Enclosure | `results/enclosure_estimate.json` |
| 12 | Power Budget | `results/power_budget.json` |
| 13 | Benchmarks | `results/summary.json`, `results/figures/` |
| 14 | Demo Script | `docs/demo_script.md` |
| 15 | Risk Register | `docs/RISK_REGISTER.md` |
| 16 | Timeline | `docs/roadmap.csv` |
| 17 | Evidence & Citations | `docs/references.md`, `docs/EVIDENCE_CONVENTIONS.md` |
| 18 | Team & Contacts | Template |

---

## Evidence Integration

### Figures (`deck/figures/generate_figures.py`)
| Figure | Source Data | Output |
|--------|-------------|--------|
| Virtual latency boxplot | `results/virtual_trials.csv` | `results/figures/virtual_latency_boxplot.png` |
| Traffic target | `results/summary.json` | `results/figures/traffic_target.png` |

### Metrics Injection
- `results/summary.json` → latency, throughput numbers
- `results/power_budget.json` → power estimate
- `results/pinmap_validation.json` → pin validation status
- `results/phase_a_audit.json` → audit status

---

## Demo Script (`docs/demo_script.md`)

Describes narrow voice-to-simulation demo:
1. "Open the amplifier project and run the simulation"
2. Host opens project, runs ngspice
3. Returns SIMULATED gain/bandwidth
4. "Show result" → cached metrics displayed

---

## Invariants

1. **Template-driven** — No slide creation from scratch
2. **Evidence-linked** — Every metric traces to results/ file
3. **Labels honest** — SIMULATED/TARGET/MEASURED on all numbers
4. **Placeholders explicit** — `[[HUMAN: ...]]` for missing data
5. **Visual QA required** — lxml rendering needs PowerPoint/LibreOffice check
6. **Citations verified** — `docs/references.md` primary sources only

---

## Test Coverage

| Test | Verifies |
|------|----------|
| `test_current_draft_has_structural_qa_invariants` | Deck structure valid |
| `make deck-draft` | Draft generation works |

---

## Failure Modes

| Condition | Behavior |
|-----------|----------|
| Template missing | Build fails |
| Placeholder not replaced | Visible in output |
| Figure generation fails | Missing plots |
| lxml rendering differs | Visual QA catches |

---

## Acceptance Criteria

- 18-slide structure mapped to evidence sources
- Figure generation specified
- Demo script referenced
- 6 invariants enumerated
- Visual QA requirement noted
- Next step (0484) can use this output