# Benchmark Evidence Specification

**Generated:** 2026-11-19T05:45:00Z
**Git Commit:** ae74c9b
**Status:** APPROVED (virtual complete, physical BLOCKED)

---

## Contract

**Scope:** Benchmark execution, evidence generation, and labeling for VaaniCore prototype.

**Purpose:** Define how performance evidence is collected and reported.

---

## Virtual Benchmarks (Complete)

### Execution (`bench/run_benchmarks.py`)
```python
def run_benchmarks(num_trials=30):
    for i in range(num_trials):
        # Run virtual device loop
        start = time.perf_counter()
        run_virtual_device_loop()
        end = time.perf_counter()
        latency_ms = (end - start) * 1000
        trials.append({"trial": i, "latency_ms": latency_ms, "label": "SIMULATED"})
```

### Output: `results/virtual_trials.csv`
```csv
trial,latency_ms,label
0,12.3,SIMULATED
1,11.8,SIMULATED
...
29,12.1,SIMULATED
```

### Validation: `bench/validate_summary.py`
```python
def validate_summary(trials_csv, output_json):
    # Compute statistics
    stats = {
        "label": "SIMULATED",
        "count": len(trials),
        "mean_ms": mean(latencies),
        "std_ms": stdev(latencies),
        "p50_ms": percentile(latencies, 50),
        "p95_ms": percentile(latencies, 95),
        "p99_ms": percentile(latencies, 99),
        "min_ms": min(latencies),
        "max_ms": max(latencies)
    }
    # Validate schema
    write_json(output_json, stats)
```

### Output: `results/summary.json`
```json
{
  "provenance": {"generated_at_utc": "...", "git_commit": "..."},
  "label": "SIMULATED",
  "count": 30,
  "mean_ms": 12.05,
  "std_ms": 0.42,
  "p50_ms": 12.0,
  "p95_ms": 12.7,
  "p99_ms": 13.1,
  "min_ms": 11.2,
  "max_ms": 13.5
}
```

### Figures: `bench/analyze.py`
- `results/figures/virtual_latency_boxplot.png` — Boxplot of 30 trials
- `results/figures/traffic_target.png` — Target vs actual throughput

---

## Physical Benchmarks (BLOCKED)

### Target Metrics (from `docs/EVIDENCE_CONVENTIONS.md`)
| Metric | Target | Label When Measured |
|--------|--------|---------------------|
| PTT-to-result latency | < 500ms | MEASURED |
| Audio capture throughput | 16kHz sustained | MEASURED |
| MFCC compute time | < 10ms/frame | MEASURED |
| Inference time | < 50ms | MEASURED |
| Serial round-trip | < 20ms | MEASURED |
| Total voice-to-result | < 1000ms | MEASURED |

### Required Evidence for MEASURED
- N ≥ 30 measurements per condition
- Instrument: oscilloscope (latency), logic analyzer (serial), power meter
- Conditions documented: temperature, voltage, firmware version
- `results/timing_study.csv` populated with raw measurements

---

## Timing Study (`bench/timing_study.csv`, `bench/analyze_timing.py`)

### Template (placeholder)
```csv
condition,trial,metric,value,unit,label
ptt_to_result,1,latency,450,ms,TARGET
mfcc_compute,1,latency,8,ms,TARGET
...
```

### Analysis
- `bench/analyze_timing.py` processes CSV → statistical summary
- Requires physical hardware measurements

---

## Invariants

1. **Label honesty** — All virtual results labeled SIMULATED
2. **Schema validation** — summary.json must pass validate_summary.py
3. **N ≥ 30** — Minimum trials for statistical validity
3. **Provenance** — Every result file has git_commit, timestamp
4. **No MEASURED without hardware** — Physical data only from instruments
5. **Reproducibility** — Same commit → same virtual results
6. **Figures match data** — Plots generated from same CSV/JSON

---

## Test Coverage

| Test | Verifies |
|------|----------|
| `test_current_summary_has_required_schema` | summary.json schema |
| `test_missing_metric_is_rejected` | Validation rejects incomplete |
| `test_numeric_rows_produce_measured_summary` | MEASURED label only for numeric |
| `test_placeholder_is_blocked` | TARGET placeholders blocked |

---

## Failure Modes

| Condition | Behavior |
|-----------|----------|
| Virtual trials fail | Exception, no output |
| Schema validation fails | validate_summary.py exits 1 |
| Physical data missing | timing_study.csv remains placeholder |
| Label mismatch | Audit flags inconsistency |

---

## Acceptance Criteria

- Virtual benchmark pipeline specified (30 trials, SIMULATED label)
- Summary schema validated
- Figures generated from data
- Physical targets defined (MEASURED requirements)
- Timing study template specified
- 6 invariants enumerated
- Physical benchmarks BLOCKED on hardware
- Next step (0524) can use this output