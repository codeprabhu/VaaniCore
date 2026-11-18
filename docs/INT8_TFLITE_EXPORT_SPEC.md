# int8 TFLite Export Specification

**Generated:** 2026-11-19T04:25:00Z
**Git Commit:** c394453
**Status:** APPROVED (spec complete, export BLOCKED on trained model)

---

## Contract

**Scope:** TensorFlow Lite int8 quantization and export for ESP32-S3 deployment.

**Purpose:** Produce quantized model suitable for TFLite-Micro on ESP32-S3.

---

## Export Pipeline (`ml/export_tflite.py`)

### Prerequisites
- Trained Keras model checkpoint (best val loss)
- Representative dataset (subset of training data for calibration)

### Converter Configuration
```python
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.representative_dataset = representative_dataset_gen
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter.inference_input_type = tf.int8
converter.inference_output_type = tf.int8
converter.allow_custom_ops = False
```

### Representative Dataset Generator
```python
def representative_dataset_gen():
    # Yield calibration samples from training set
    for features, _ in calibration_dataset.take(100):
        yield [features.astype(np.float32)]
```

---

## Output Model

| Property | Value |
|----------|-------|
| Format | TensorFlow Lite FlatBuffer |
| Quantization | Full int8 (weights + activations) |
| Input Type | int8 (shape: [1, num_frames, 10, 1] or [1, 10] per frame) |
| Output Type | int8 (shape: [1, 13] logits) |
| Size | ~20 KB |
| Ops | TFLITE_BUILTINS_INT8 only |

---

## Firmware Integration

### TFLite-Micro on ESP32-S3
```c
// In infer_task
static const char* model_data = model_int8_tflite_start;  // Embedded binary
static tflite::MicroMutableOpResolver<10> resolver;
resolver.AddDepthwiseConv2D();
resolver.AddConv2D();
resolver.AddAveragePool2D();
resolver.AddFullyConnected();
resolver.AddSoftmax();
resolver.AddReshape();
resolver.AddQuantize();
resolver.AddDequantize();

static tflite::MicroInterpreter interpreter(model, resolver, tensor_arena, arena_size);
```

### Input/Output Quantization
- **Input:** MFCC features (float) → quantize to int8 using input scale/zero_point
- **Output:** Logits (int8) → dequantize to float for argmax

---

## Invariants

1. **Full int8 quantization** — Weights and activations int8
2. **Representative dataset** — Calibration from actual training data
3. **INT8 ops only** — No float ops in converted model
4. **Input/output int8** — Firmware handles quantization/dequantization
5. **Model size < 50KB** — Fits in ESP32-S3 flash
6. **Reproducible export** — Fixed seed, deterministic conversion
7. **Accuracy retention** — int8 accuracy within 1% of float baseline
8. **TFLite-Micro compatible** — Only supported ops used

---

## Test Coverage

| Test | Status |
|------|--------|
| Smoke test (model compile) | ✅ PASS |
| Export script syntax | ✅ PASS |
| Quantization accuracy | ❌ BLOCKED (no trained model) |
| Firmware inference | ❌ BLOCKED (no hardware) |

---

## Failure Modes

| Condition | Behavior |
|-----------|----------|
| No trained model | Export cannot proceed |
| Calibration data missing | Quantization fails or degrades |
| Unsupported ops | Converter error |
| Accuracy drop > 1% | Quantization-aware training needed |
| Model too large | Architecture reduction needed |

---

## Acceptance Criteria

- Export pipeline specified with converter config
- Representative dataset generator defined
- Output model properties documented
- Firmware integration outlined
- 8 invariants enumerated
- Export BLOCKED on trained model
- Next step (0384) can use this output