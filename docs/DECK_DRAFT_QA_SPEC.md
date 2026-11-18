# Deck Draft and QA Specification

**Generated:** 2026-11-19T05:25:00Z
**Git Commit:** d6536ed
**Status:** APPROVED

---

## Contract

**Scope:** Presentation deck draft generation and quality assurance process.

**Purpose:** Define how the submission deck is built and validated.

---

## Draft Generation (`deck/build_deck.py`)

### Command
```bash
# Draft (with placeholders)
make deck-draft
# or
python3 deck/build_deck.py --draft

# Final (all placeholders filled)
make deck-final
# or
python3 deck/build_deck.py --final
```

### Process
1. Load template: `inputs/Vishwakarma_Awards_2026-27_Stage_2_Submission_Template.pptx`
2. Parse OOXML with lxml
3. Replace placeholders:
   - `[[METRIC_...]]` → values from `results/summary.json`, `results/power_budget.json`, etc.
   - `[[FIGURE_...]]` → images from `results/figures/`
   - `[[CITATION_...]]` → entries from `docs/references.md`
   - `[[HUMAN: ...]]` → left as-is in draft, must be filled for final
4. Write output: `deck/out/Vishwakarma_Stage2_VaaniCore.pptx`

---

## Placeholder Categories

| Prefix | Source | Example |
|--------|--------|---------|
| `[[METRIC_` | `results/summary.json`, `results/power_budget.json` | `[[METRIC_LATENCY_P50]]` |
| `[[FIGURE_` | `results/figures/*.png` | `[[FIGURE_LATENCY_BOXPLOT]]` |
| `[[CITATION_` | `docs/references.md` | `[[CITATION_ESP32_DATASHEET]]` |
| `[[HUMAN_` | Manual input required | `[[HUMAN:APPLICATION_ID]]` |

---

## QA Checklist (`deck/out/DRAFT_STATUS.md`, `docs/SUBMISSION_CHECKLIST.md`)

### Draft QA (`make deck-draft` → visual inspection)
- [ ] All slides render without corruption
- [ ] Figures visible and scaled correctly
- [ ] Metrics match `results/*.json` values
- [ ] Citations match `docs/references.md`
- [ ] `[[HUMAN: ...]]` placeholders identified
- [ ] Slide count = 18
- [ ] No text overflow/corruption

### Final QA (`make deck-final` → submission)
- [ ] All `[[HUMAN: ...]]` placeholders replaced
- [ ] All metrics verified against evidence
- [ ] All figures high-resolution
- [ ] Citations formatted per template style
- [ ] Visual review in PowerPoint/LibreOffice
- [ ] File size within limits
- [ ] No template artifacts

---

## Submission Checklist (`docs/SUBMISSION_CHECKLIST.md`)

| Category | Required | Status |
|----------|----------|--------|
| Application metadata | ID, institution, track, mentor, deadline | `[[HUMAN: ...]]` |
| Primary evidence | Hardware photos, measurements, citations | `[[HUMAN: ...]]` |
| Deck | Final PPTX with all placeholders filled | Draft only |
| Code | Repository tagged, reproducible | Ready |
| Hardware | Schematic, layout, BOM, enclosure | BLOCKED |

---

## Invariants

1. **Template fidelity** — lxml preserves theme/assets
2. **Evidence traceability** — Every metric → results/ file
3. **Placeholder honesty** — `[[HUMAN: ...]]` not hidden in draft
4. **Visual QA mandatory** — lxml rendering not pixel-perfect
5. **Citation accuracy** — Primary sources only (`docs/references.md`)
6. **Final = submission-ready** — No placeholders in final

---

## Test Coverage

| Test | Verifies |
|------|----------|
| `test_current_draft_has_structural_qa_invariants` | Draft structure valid |
| `make deck-draft` | Generation works |

---

## Failure Modes

| Condition | Behavior |
|-----------|----------|
| Template missing | Build fails |
| Placeholder not found | Left as-is (visible in draft) |
| Figure missing | Blank placeholder |
| lxml rendering differs | Visual QA catches |
| Final has placeholders | Rejected by checklist |

---

## Acceptance Criteria

- Draft generation process specified
- Placeholder categories defined
- QA checklist documented
- Submission checklist referenced
- 6 invariants enumerated
- Visual QA requirement explicit
- Next step (0504) can use this output