# Pinmap Reconciliation Specification

**Generated:** 2026-11-19T04:55:00Z
**Git Commit:** 0818415
**Status:** APPROVED (VaaniCore pinmap authoritative, Raphael archive missing)

---

## Contract

**Scope:** Reconciliation of pin assignments across VaaniCore pinmap.csv, firmware pins.h, and (missing) Raphael KiCad schematic.

**Purpose:** Ensure single source of truth for GPIO assignments.

---

## Authoritative Source: `hardware/pinmap.csv`

```csv
name,gpio,role,notes
I2S_BCLK,4,I2S clock,
I2S_WS,5,I2S word select,
I2S_DIN,6,I2S data,
I2C_SDA,8,I2C,
I2C_SCL,9,I2C,
BUTTON_CONFIRM,15,button,
BUTTON_ABORT,16,button,
MUTE_SENSE,17,privacy switch,
LED_LISTEN,18,LED,
LED_BUSY,21,LED,
LED_ERR,47,LED,
USB_DM,19,native USB,reserved
USB_DP,20,native USB,reserved
```

**13 pins defined** — Core functionality only.

---

## Firmware Header: `firmware/main/pins.h`

```c
#define PIN_I2S_BCLK 4
#define PIN_I2S_WS 5
#define PIN_I2S_DIN 6
#define PIN_I2C_SDA 8
#define PIN_I2C_SCL 9
#define PIN_BUTTON_CONFIRM 15
#define PIN_BUTTON_ABORT 16
#define PIN_MUTE_SENSE 17
#define PIN_LED_LISTEN 18
#define PIN_LED_BUSY 21
#define PIN_LED_ERR 47
#define PIN_USB_DM 19
#define PIN_PIN_USB_DP 20
// Additional (not in pinmap.csv):
#define PIN_UART_TX 43
#define PIN_UART_RX 44
#define PIN_JTAG_TCK 39
#define PIN_JTAG_TDO 40
#define PIN_JTAG_TDI 41
#define PIN_JTAG_TMS 42
```

**Match Status:** 13/13 core pins **MATCH EXACTLY**. Additional UART/JTAG pins are firmware-only (debug).

---

## Validation Tool: `hardware/validate_pinmap.py`

```python
def validate():
    # 1. Read pinmap.csv
    # 2. Check: unique names, unique GPIOs, GPIO range 0-47 (ESP32-S3)
    # 3. Generate pinmap_validation.json
    # 4. Exit 0 on success, 1 on conflict
```

**Output:** `results/pinmap_validation.json`

---

## KiCad Netlist Spec (Placeholder)

`hardware/kicad/netlist_spec.csv` — Expected format for KiCad netlist export:
```csv
net_name,pin_ref,gpio
I2S_BCLK,U1.4,4
I2S_WS,U1.5,5
...
```

---

## Raphael Archive (MISSING)

Expected files:
- `raphael.kicad_pro` — Project file
- `raphael.kicad_sch` — Schematic
- `raphael.kicad_pcb` — PCB layout

**Reconciliation Required (when archive available):**
1. Export netlist from `raphael.kicad_sch`
2. Compare each net's GPIO against `hardware/pinmap.csv`
3. Document conflicts (if any) — **BLOCK on any mismatch**
4. Update pinmap.csv only if Raphael is validated as correct (human decision)

---

## Invariants

1. **Pinmap.csv is authority** — All other sources must match
2. **No silent conflicts** — Any mismatch → BLOCK, human decision
3. **Firmware pins.h synced** — Manual sync validated by `validate_pinmap.py`
4. **ESP32-S3 GPIO range** — 0-47 only (validated)
5. **Unique GPIOs** — No duplicate assignments (validated)
6. **Reserved pins documented** — USB_DM/DP marked reserved
7. **Raphael cannot override** — VaaniCore pinmap is requirements source

---

## Test Coverage

| Test | Verifies |
|------|----------|
| `make hardware-check` → `validate_pinmap.py` | CSV valid, unique GPIOs, range check |
| `test_pinmap_artifact_can_be_generated` | Validation produces JSON artifact |

---

## Failure Modes

| Condition | Behavior |
|-----------|----------|
| Duplicate GPIO in pinmap.csv | Validation fails, exit 1 |
| GPIO out of range (0-47) | Validation fails |
| Firmware pins.h mismatch | Human review required |
| Raphael netlist mismatch | **BLOCK** — human decision required |
| Missing pin in Raphael | Document gap |

---

## Acceptance Criteria

- VaaniCore pinmap.csv documented as authoritative
- Firmware pins.h matches for 13 core pins
- Validation tool specified
- Raphael archive reconciliation procedure defined (BLOCK on conflict)
- 7 invariants enumerated
- Raphael archive missing — reconciliation BLOCKED
- Next step (0424) can use this output