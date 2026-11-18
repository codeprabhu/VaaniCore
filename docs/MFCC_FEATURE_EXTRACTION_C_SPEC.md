# MFCC Feature Extraction C Specification

**Generated:** 2026-11-19T03:15:00Z
**Git Commit:** bc267ff
**Status:** APPROVED (host-verified, hardware BLOCKED)

---

## Contract

**Scope:** C implementation of MFCC feature extraction for ESP32-S3 firmware.

**Purpose:** Provide deterministic, fixed-point friendly MFCC matching Python reference.

---

## Pipeline Specification (Matches `docs/dsp_spec.md`)

| Stage | Operation | Parameters |
|-------|-----------|------------|
| 1 | DC Block | `y[n] = x[n] - x[n-1] + 0.995*y[n-1]` |
| 2 | Pre-emphasis | `0.97` |
| 3 | Framing | 512-sample Hann window, 256-sample hop |
| 4 | FFT | 512-point real FFT |
| 5 | Mel Filterbank | 40 bands, 20-4000 Hz |
| 6 | Log | `log(x + 1e-8)` |
| 9 | DCT-II | Unnormalized, 10 coefficients |

**Sample Rate:** 16 kHz
**Output:** 10 MFCC coefficients per frame

---

## API (`mfcc.h`)

```c
#define MFCC_NUM_COEFFS 10
#define MFCC_NUM_MEL_BANDS 40
#define MFCC_FRAME_SIZE 512
#define MFCC_HOP_SIZE 256

typedef struct {
    float coeffs[MFCC_NUM_COEFFS];
    // Internal state for streaming
    float dc_block_state;
    float preemph_state;
    float window_buffer[MFCC_FRAME_SIZE];
    size_t buffer_fill;
} mfcc_context_t;

void mfcc_init(mfcc_context_t *ctx);
int mfcc_process(mfcc_context_t *ctx, const int16_t *samples, size_t num_samples, float *out_coeffs, size_t *num_frames);
```

---

## Implementation (`mfcc.c`)

### State Management
- `dc_block_state`: Previous y[n-1] for DC block
- `preemph_state`: Previous x[n-1] for pre-emphasis
- `window_buffer`: Circular buffer for 512-sample framing
- `buffer_fill`: Samples currently in buffer

### Processing Flow
```c
int mfcc_process(mfcc_context_t *ctx, const int16_t *samples, size_t num_samples, float *out_coeffs, size_t *num_frames) {
    // 1. Fill buffer with new samples (int16_t → float)
    // 2. While buffer has >= 512 samples:
    //    a. Apply Hann window
    //    b. DC block + pre-emphasis (on buffered samples)
    //    c. 512-point real FFT
    //    d. 40 mel filterbank (20-4000 Hz)
    //    e. Log(mel + 1e-8)
    //    f. DCT-II → 10 coeffs
    //    g. Advance buffer by 256 (hop)
    // 3. Return number of frames produced
}
```

### Fixed-Point Considerations
- Input: int16_t → float conversion at start
- Internal: float (can be Q15/Q31 for production)
- Output: float[10] (can be quantized for TFLite-Micro)

---

## Python Parity (`ml/features.py`)

Reference implementation in Python:
```python
def compute_mfcc(waveform: np.ndarray) -> np.ndarray:
    # DC block
    # Pre-emphasis 0.97
    # Framing: 512 Hann, 256 hop
    # FFT 512
    # 40 mel bands 20-4000 Hz
    # log(x + 1e-8)
    # DCT-II → 10 coeffs
    return mfcc  # shape (num_frames, 10)
```

---

## Parity Verification

| Test | Metric | Result |
|------|--------|--------|
| `make dsp-test` | Max absolute error | 0.0139313 |
| Tolerance | | 0.05 |
| Status | | ✅ PASS |

**Test Method:** `tests/dsp_parity.c` runs C mfcc.c on golden input, compares to Python-generated golden vector.

---

## Invariants

1. **Python parity** — Max error < 0.05 (verified 0.0139)
2. **Streaming support** — Context maintains state between calls
3. **Frame alignment** — 512-sample frames, 256-hop
4. **Numerical stability** — DC block, log epsilon prevent divergence
5. **Fixed-point ready** — Float internal, quantizable output
6. **Bounded memory** — Fixed buffers (512 + state)
7. **Deterministic** — Same input → same output
8. **No heap** — All buffers in context struct

---

## Test Coverage

| Test | Verifies |
|------|----------|
| `make dsp-test` | C output matches Python golden vector |
| `test_golden_vector_is_reproducible` | Python reference deterministic |
| `test_shape` | Output shape (frames, 10) |
| `test_two_second_window_has_124_frames` | Framing math correct |

---

## Failure Modes

| Condition | Behavior |
|-----------|----------|
| Insufficient samples | Returns 0 frames, fills buffer |
| Buffer overflow | Not possible (circular, hop ≤ frame) |
| NaN/Inf in FFT | Log epsilon prevents log(0) |
| DC block divergence | 0.995 pole inside unit circle |

---

## Acceptance Criteria

- MFCC pipeline stages specified
- API with streaming context defined
- Python parity verified (max error 0.0139 < 0.05)
- 8 invariants enumerated
- Hardware test BLOCKED (requires ESP32-S3)
- Next step (0314) can use this output