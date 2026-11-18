# Evidence Conventions

**Generated:** 2026-11-18T23:20:00Z
**Git Commit:** a407329
**Status:** APPROVED

---

## Directory Structure

```
results/
├── *.json              # Structured evidence (audit, validation, estimates)
├── *.csv               # Tabular evidence (trials, timing study)
├── figures/
│   └── *.png           # Generated plots
├── deck/
│   └── *.pptx          # Presentation artifacts
logs/
├── *.jsonl             # Audit logs (append-only)
docs/evidence/          # Human-collected evidence (photos, measurements) - to be created
```

---

## Label Taxonomy (Mandatory)

Every quantitative result **must** carry exactly one label:

| Label | Meaning | When to Use |
|-------|---------|-------------|
| **MEASURED** | Physical hardware, documented instruments, recorded conditions | Only for data from identified physical ESP32-S3, oscilloscope, multimeter, etc. |
| **SIMULATED** | Software-only virtual device, no hardware involved | Virtual device loop, host-only benchmarks, CI runs |
| **TARGET** | Analytical estimate, design goal, not yet validated | Power budget, enclosure estimates, timing study placeholders |
| **ESTIMATED** | Rough calculation with stated assumptions | Early sizing, vendor datasheet projections |

**Forbidden:** Unlabeled numbers, "preliminary", "expected", "~", "approx" without explicit label.

---

## File Naming Convention

| Pattern | Example | Description |
|---------|---------|-------------|
| `{domain}_{metric}.json` | `power_budget.json`, `pinmap_validation.json` | Structured evidence |
| `{domain}_trials.csv` | `virtual_trials.csv` | Repeated measurements |
| `{domain}_study.csv` | `timing_study.csv` | Parameter sweeps |
| `phase_{X}_audit.json` | `phase_a_audit.json` | Phase gate evidence |
| `figure_{description}.png` | `figure_virtual_latency_boxplot.png` | Generated plots |
| `host_agent_{date}.jsonl` | `host_agent_20261118.jsonl` | Audit logs (date-stamped) |

---

## JSON Schema Requirements

All `.json` evidence files **must** include:

```json
{
  "provenance": {
    "generated_at_utc": "ISO8601",
    "git_commit": "short_hash",
    "config": { ... }
  },
  "label": "MEASURED|SIMULATED|TARGET|ESTIMATED",
  "data": { ... }
}
```

Example: `results/phase_a_audit.json` (see repository)

---

## Audit Log Format (JSONL)

Each line in `logs/host_agent.jsonl`:

```json
{
  "timestamp": "ISO8601",
  "direction": "device_to_host|host_to_device|host_error",
  "frame": { "seq": 1, "verb": "PING", "fields": {} },
  "error": "optional error string"
}
```

**Never** include audio payloads, raw samples, or PII.

---

## Human Evidence Requirements

For MEASURED claims, `docs/evidence/` must contain:

| Evidence Type | Format | Metadata Required |
|---------------|--------|-------------------|
| Hardware photos | JPEG/PNG | Device ID, date, lighting, scale |
| Oscilloscope captures | PNG/CSV | Instrument model, settings, probe |
| Multimeter readings | CSV | Instrument model, range, leads |
| Timing study | CSV | `bench/timing_study.csv` schema |
| Mentor sign-off | PDF/scan | Name, date, signature |
| Vendor quotes | PDF | Vendor, part number, price, date, validity |

---

## Provenance Tracking

Use `tools/provenance.py` to record:

- Source of each data point
- Tool version used
- Human operator (if manual)
- Environmental conditions

---

## Enforcement

- `bench/validate_summary.py` rejects summary.json without required schema and label
- `tools/audit_phase_a.py` checks for explicit SIMULATED/TARGET labels
- CI fails if evidence conventions violated

---

## Acceptance Criteria

- Convention document approved and stored
- All existing evidence files comply (or documented exceptions)
- Validation tools enforce conventions
- Next step (0084) can use this output