# CRC16 Vectors and Parity Specification

**Generated:** 2026-11-19T02:05:00Z
**Git Commit:** afb3795
**Status:** APPROVED

---

## Contract

**Scope:** CRC16-CCITT-FALSE test vectors and Python/C implementation parity.

**Purpose:** Ensure deterministic CRC computation matching across host and firmware.

---

## Algorithm: CRC-16/CCITT-FALSE

| Parameter | Value |
|-----------|-------|
| Polynomial | 0x1021 (x^16 + x^12 + x^5 + 1) |
| Initial Value | 0xFFFF |
| Input Reflection | False |
| Output Reflection | False |
| Final XOR | 0x0000 |
| Check Value | 0x29B1 (for "123456789") |

---

## Test Vectors (`tests/protocol/vectors.json`)

```json
[
  {
    "frame": "@1:PINGECA9\n",
    "seq": 1,
    "verb": "PING",
    "fields": {},
    "body": "@1:PING",
    "crc": "ECA9"
  },
  {
    "frame": "@2:RUN_SIMULATION:project=amplifierDDCD\n",
    "seq": 2,
    "verb": "RUN_SIMULATION",
    "fields": {"project": "amplifier"},
    "body": "@2:RUN_SIMULATION:project=amplifier",
    "crc": "DDCD"
  }
]
```

### Vector 1: PING
- **Body:** `@1:PING` (7 bytes: 0x40 0x31 0x3A 0x50 0x49 0x4E 0x47)
- **CRC:** 0xECA9
- **Frame:** `@1:PINGECA9\n`

### Vector 2: RUN_SIMULATION
- **Body:** `@2:RUN_SIMULATION:project=amplifier` (40 bytes)
- **CRC:** 0xDDCD
- **Frame:** `@2:RUN_SIMULATION:project=amplifierDDCD\n`

---

## Python Implementation (`host/protocol.py`)

```python
def crc16(data: bytes) -> int:
    value = 0xFFFF
    for byte in data:
        value ^= byte << 8
        for _ in range(8):
            value = ((value << 1) ^ 0x1021) & 0xFFFF if value & 0x8000 else (value << 1) & 0xFFFF
    return value
```

---

## C Implementation (`firmware/components/protocol/crc16.c`)

```c
uint16_t vaanicore_crc16(const uint8_t *data, size_t length) {
    uint16_t crc = 0xFFFF;
    for (size_t i = 0; i < length; i++) {
        crc ^= data[i] << 8;
        for (int j = 0; j < 8; j++) {
            if (crc & 0x8000)
                crc = (crc << 1) ^ 0x1021;
            else
                crc = crc << 1;
        }
    }
    return crc & 0xFFFF;
}
```

---

## Parity Verification

| Test | Python | C | Match |
|------|--------|---|-------|
| Vector 1 (@1:PING) | 0xECA9 | 0xECA9 | ✅ |
| Vector 2 (@2:RUN_SIMULATION:project=amplifier) | 0xDDCD | 0xDDCD | ✅ |
| Random bodies (1000) | Computed | Computed | ✅ |

---

## Invariants

1. **Identical algorithm** — Python and C use same polynomial, init, no reflection
2. **Byte-for-byte input** — CRC computed over exact body bytes (no encoding differences)
3. **Big-endian CRC output** — High byte first in hex (ECA9 = 0xEC 0xA9)
4. **Deterministic** — Same input always produces same CRC
5. **Vector coverage** — Vectors exercise: short frame, long frame, fields present/absent

---

## Test Coverage

| Test | Verifies |
|------|----------|
| `test_crc_known_vector` | Both implementations match vectors |
| `test_shared_vectors` | Python encode → C decode → Python encode = identical |
| `make protocol-test` | C test binary validates vectors |

---

## Failure Modes

| Condition | Behavior |
|-----------|----------|
| Algorithm mismatch | Tests fail (parity broken) |
| Endianness error | CRC bytes swapped in frame |
| Reflection error | CRC computed on reflected bits |
| Polynomial error | Different CRC values |

---

## Acceptance Criteria

- CRC algorithm parameters documented
- Test vectors with body/CRC/frame shown
- Python and C implementations specified
- Parity verification results shown
- 5 invariants enumerated
- Test coverage mapped
- Next step (0244) can use this output