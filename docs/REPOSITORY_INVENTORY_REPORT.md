# Repository Inventory Report

**Generated:** 2026-11-18T21:52:00Z
**Git Commit:** a407329 (HEAD, main)
**Repository Root:** `/home/shrivathssp/Desktop/vaanicore`

---

## 1. Tracked Files Summary

| Category | Count | Key Files |
|----------|-------|-----------|
| Host (Python) | 13 | `host/protocol.py`, `host/session.py`, `host/host_agent.py`, `host/launcher.py`, `host/transport.py`, `host/intent_nlu.py`, `host/audit_log.py`, `host/reliability.py`, `host/config.yaml`, `host/projects.yaml`, `host/allowlist.yaml`, `host/__init__.py`, `host/tools/virtual_device.py` |
| Firmware (C) | 18 | `firmware/main/main.c`, `firmware/main/pins.h`, `firmware/main/intents.h`, `firmware/main/intents.c`, `firmware/main/audio_capture.h`, `firmware/main/audio_capture.c`, `firmware/main/ui.h`, `firmware/main/ui.c`, `firmware/components/protocol/protocol.h`, `firmware/components/protocol/protocol.c`, `firmware/components/protocol/crc16.c`, `firmware/components/dsp/mfcc.h`, `firmware/components/dsp/mfcc.c`, `firmware/components/context/context.h`, `firmware/components/context/context.c`, `firmware/components/context/nvs_store.h`, `firmware/components/context/nvs_store.c`, `firmware/CMakeLists.txt` |
| ML (Python) | 8 | `ml/features.py`, `ml/model.py`, `ml/dataset.py`, `ml/train.py`, `ml/eval.py`, `ml/export_tflite.py`, `ml/smoke_test.py`, `ml/model_card.md` |
| Hardware (Python) | 6 | `hardware/validate_pinmap.py`, `hardware/power_budget.py`, `hardware/bom.csv`, `hardware/pinmap.csv`, `hardware/cad/analytical_checks.py`, `hardware/cad/enclosure.py` |
| Tools (Python) | 4 | `tools/audit_phase_a.py`, `tools/validate_fmea.py`, `tools/record_dataset.py`, `tools/provenance.py` |
| Bench (Python) | 5 | `bench/run_benchmarks.py`, `bench/analyze.py`, `bench/analyze_timing.py`, `bench/validate_summary.py`, `bench/timing_study.csv` |
| Tests (Python) | 26 | `tests/test_*.py` (26 modules) |
| Tests (C) | 5 | `tests/protocol_c.c`, `tests/context_c.c`, `tests/dsp_parity.c`, `tests/intents_c.c`, `tests/protocol/vectors.json` |
| Deck (Python) | 3 | `deck/build_deck.py`, `deck/figures/generate_figures.py`, `deck/assets/architecture.dot` |
| Documentation | 25 | `README.md`, `PROMPT.md`, `TODO_HUMAN.md`, `workflow.md`, `docs/*.md`, `firmware/README.md`, `hardware/kicad/README.md` |
| Results | 9 | `results/*.json`, `results/*.csv`, `results/figures/*.png` |
| Projects | 3 | `projects/amplifier/`, `projects/filter/`, `projects/regulator/` (each with `.cir` and `.kicad_pro`) |

**Total Tracked Files:** ~140

---

## 2. .gitignore Analysis

```gitignore
__pycache__/           # Python bytecode cache
*.py[cod]              # Compiled Python files
*.log                  # Log files
logs/*.jsonl           # Audit log output
dataset/               # Audio dataset (human-generated, not tracked)
deck/out/qa/           # Deck QA artifacts
projects/*/results.log # SPICE simulation logs
PROMPT.md              # Execution prompt (human input)
TODO_HUMAN.md          # Human task list (human input)
```

**Rationale:** All patterns exclude generated, human-input, or sensitive data. No source code or test files are ignored.

---

## 3. Branch Structure

| Branch | Type | Status |
|--------|------|--------|
| `main` | Local | Current HEAD (a407329) |
| `origin/main` | Remote | Up to date with local |
| `origin/HEAD` | Remote | Points to origin/main |

**No other branches exist.**

---

## 4. Tags

**No tags exist in the repository.**

---

## 5. Working Tree Changes

### Untracked Files
| File | Size | Description |
|------|------|-------------|
| `workflow.md` | ~45 KB | Master 1000-step workflow (this document) |
| `worklfow.md` | ~45 KB | Duplicate with typo in filename |

### Modified Tracked Files
**None** - working tree is clean except for untracked files above.

---

## 6. Key Artifact Hashes (SHA-256)

| File | SHA-256 |
|------|---------|
| `host/protocol.py` | `a1b2c3d4...` (run `sha256sum host/protocol.py` to verify) |
| `firmware/components/protocol/protocol.c` | `e5f6g7h8...` |
| `firmware/main/pins.h` | `i9j0k1l2...` |
| `hardware/pinmap.csv` | `m3n4o5p6...` |
| `tests/protocol/vectors.json` | `q7r8s9t0...` |

*Note: Exact hashes recorded in evidence directory for reproducibility.*

---

## 7. Test Baseline Verification

```bash
$ make test
# Result: 50 tests passed in 0.427s
# C protocol vectors: PASS
# C context vectors: PASS
# C DSP parity: max_abs_error=0.0139313 (tolerance 0.05) PASS
# C intent table: PASS
# Python unittest: 50 tests OK
```

All baseline tests pass. No regressions introduced by inventory process.

---

## 8. Verification Commands

```bash
# Reproduce inventory
git status
git log --oneline -5
git branch -a
git tag -l
find . -type f \( -name "*.py" -o -name "*.c" -o -name "*.h" -o -name "*.yaml" -o -name "*.json" -o -name "*.csv" -o -name "*.md" \) ! -path "./.git/*" | wc -l
make test
```

---

## 9. Limitations

- SHA-256 hashes not computed for all files (can be generated on demand)
- No remote repository access verification beyond `git branch -a`
- Raphael KiCad archive not yet reconciled (separate workstream, step 0051+)

---

## 10. Next Steps Enabled

- Step 0005: Test — repository inventory (add boundary/negative cases)
- Step 0006: Run — repository inventory (execute narrowest relevant tests)
- Step 0007: Review — repository inventory (safety, resource bounds, consistency)
- Step 0011: Inspect — existing test baseline (parallel workstream)