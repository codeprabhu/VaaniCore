# DS-CNN Training Pipeline Specification

**Generated:** 2026-11-19T04:15:00Z
**Git Commit:** c394453
**Status:** APPROVED (architecture defined, training BLOCKED on dataset)

---

## Contract

**Scope:** Depthwise Separable CNN training for intent classification.

**Purpose:** Define model architecture, training procedure, and evaluation protocol.

---

## Model Architecture (`ml/model.py`)

### DS-CNN (Depthwise Separable CNN)
Based on "DS-CNN: Deep Separable CNN for Keyword Spotting" (Tang et al.)

```python
class DSCNN(nn.Module):
    def __init__(self, num_classes=13, input_channels=1):
        # Input: (batch, 1, num_frames, 10)  # MFCC: 10 coeffs
        self.conv1 = Conv2d(1, 64, kernel_size=(3,3), padding=1)
        self.dw_conv1 = DepthwiseSeparableConv2d(64, 64, kernel_size=(3,3))
        self.dw_conv2 = DepthwiseSeparableConv2d(64, 128, kernel_size=(3,3), stride=2)
        self.dw_conv3 = DepthwiseSeparableConv2d(128, 128, kernel_size=(3,3))
        self.dw_conv4 = DepthwiseSeparableConv2d(128, 256, kernel_size=(3,3), stride=2)
        self.pool = AdaptiveAvgPool2d((1,1))
        self.fc = Linear(256, num_classes)
```

### Parameters
- **Total params:** ~20k (suitable for TFLite-Micro)
- **Input:** (batch, 1, num_frames, 10) — MFCC features
- **Output:** (batch, 13) — Logits for 13 intent classes

---

## Training Config (`ml/configs/default.json`)

```json
{
  "model": "ds_cnn",
  "num_classes": 13,
  "input_shape": [null, 10],  # (frames, 10)
  "learning_rate": 0.001,
  "batch_size": 32,
  "epochs": 50,
  "optimizer": "adam",
  "loss": "cross_entropy",
  "early_stopping_patience": 10,
  "early_stopping_metric": "val_loss",
  "speaker_split": true,
  "leave_one_speaker_out": true
}
```

---

## Training Loop (`ml/train.py`)

```python
def train():
    # 1. Load speaker-split dataset
    train_ds, val_ds, test_ds = load_dataset()
    
    # 2. Create data loaders
    train_loader = DataLoader(train_ds, batch_size=32, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=32)
    
    # 3. Model, optimizer, loss
    model = DSCNN(num_classes=13)
    optimizer = Adam(model.parameters(), lr=0.001)
    criterion = CrossEntropyLoss()
    
    # 4. Training with early stopping
    best_val_loss = inf
    patience = 0
    for epoch in range(50):
        train_loss = train_epoch(model, train_loader, optimizer, criterion)
        val_loss, val_acc = evaluate(model, val_loader, criterion)
        
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            patience = 0
            save_checkpoint(model)
        else:
            patience += 1
            if patience >= 10:
                break
```

---

## Evaluation Protocol: Leave-One-Speaker-Out

| Fold | Train Speakers | Test Speaker |
|------|----------------|--------------|
| 1 | speaker2, speaker3 | speaker1 |
| 2 | speaker1, speaker3 | speaker2 |
| 3 | speaker1, speaker2 | speaker3 |

**Metrics per fold:** Accuracy, F1-score (macro), Confusion matrix
**Final metric:** Mean ± std across 3 folds

---

## Export to TFLite (`ml/export_tflite.py`)

```python
def export_tflite(model_path, output_path):
    model = load_model(model_path)
    # Convert to TFLite with int8 quantization
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.representative_dataset = representative_dataset_gen
    converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
    converter.inference_input_type = tf.int8
    converter.inference_output_type = tf.int8
    tflite_model = converter.convert()
    save_tflite(tflite_model, output_path)
```

**Output:** `model_int8.tflite` (~20KB, int8 quantized)

---

## Invariants

1. **Speaker-split only** — No random sample split
2. **Leave-one-speaker-out** — 3-fold CV, each speaker tested once
3. **Early stopping** — Prevents overfitting on small dataset
4. **Int8 quantization** — Required for ESP32-S3 TFLite-Micro
5. **Model size < 50KB** — Fits in firmware flash
6. **Reproducible** — Fixed seeds, deterministic ops
7. **Class balance** — All 13 classes represented per speaker
8. **Consent documented** — All speakers consented

---

## Test Coverage

| Test | Verifies |
|------|----------|
| `ml/smoke_test.py` | Model compiles, forward pass works |
| `test_missing_metadata_writes_non_result_status` | Eval gate blocks incomplete |

---

## Failure Modes

| Condition | Behavior |
|-----------|----------|
| Dataset not collected | Training cannot start |
| < 3 speakers | Leave-one-out impossible |
| Class imbalance | Weighted loss or oversampling needed |
| Overfitting | Early stopping triggers |
| Quantization accuracy drop | Quantization-aware training needed |

---

## Acceptance Criteria

- DS-CNN architecture specified
- Training config documented
- Leave-one-speaker-out protocol defined
- TFLite int8 export specified
- 8 invariants enumerated
- Training BLOCKED on dataset (3 speakers, 1440 clips)
- Next step (0374) can use this output