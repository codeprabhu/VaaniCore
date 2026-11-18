# Protocol Encode/Decode C Specification

**Generated:** 2026-11-19T01:55:00Z
**Git Commit:** afb3795
**Status:** APPROVED

---

## Contract

**Scope:** C implementation of VaaniCore frame encoding/decoding with CRC16.

**Purpose:** Provide bounded, heap-free protocol codec for ESP32-S3 firmware matching Python reference.

---

## Data Structures

### `vaanicore_frame_t` (protocol.h)
```c
#define VAANICORE_MAX_FRAME 128
#define VAANICORE_MAX_VERB 16
#define VAANICORE_MAX_FIELDS 64

typedef struct {
    uint8_t seq;
    char verb[VAANICORE_MAX_VERB + 1];
    char fields[VAANICORE_MAX_FIELDS + 1];  // "k=v,k=v" format
} vaanicore_frame_t;
```

---

## API

### `int vaanicore_encode_frame(uint8_t seq, const char *verb, const char *fields, char *out, size_t capacity)`
Encodes a frame into output buffer.

**Parameters:**
- `seq`: Sequence number (0-255)
- `verb`: Verb string (max 16 chars, alnum/underscore)
- `fields`: Fields string "k=v,k=v" or NULL/empty (max 64 chars)
- `out`: Output buffer
- `capacity`: Buffer capacity (must be >= 7)

**Returns:** Total frame length on success, -1 on error.

**Algorithm:**
```c
// 1. Build body: "@seq:verb" or "@seq:verb:fields"
body_len = fields ? snprintf(out, capacity, "@%u:%s:%s", seq, verb, fields)
                : snprintf(out, capacity, "@%u:%s", seq, verb);

// 2. Validate body length
if (body_len < 0 || body_len > 123 || body_len + 6 > capacity) return -1;

// 3. Compute CRC16 over body
crc = vaanicore_crc16((uint8_t *)out, body_len);

// 4. Append CRC + newline
total = snprintf(out + body_len, capacity - body_len, "%04X\n", crc);

// 5. Validate total length
return (total < 0 || body_len + total > capacity) ? -1 : body_len + total;
```

### `int vaanicore_decode_frame(const char *line, size_t length, vaanicore_frame_t *out)`
Decodes a frame from input buffer.

**Parameters:**
- `line`: Input frame (null-terminated or length given)
- `length`: Input length
- `out`: Output frame struct

**Returns:** 0 on success, -1 on format error, -2 on CRC error.

**Algorithm:**
```c
// 1. Basic validation
if (!line || !out || length < 8 || length > 128 || line[0] != '@' || line[length-1] != '\n') return -1;

// 2. Extract body and CRC
body_len = length - 5;  // exclude CRC(4) + newline(1)
parse 4 hex chars at line[body_len..body_len+3] → expected_crc
if (invalid hex) return -1;

// 3. Verify CRC
if (vaanicore_crc16((uint8_t *)line, body_len) != expected_crc) return -2;

// 4. Parse sequence (digits after '@')
find first ':' → colon
seq_str = line[1..colon-1] (max 3 digits)
seq = strtoul(seq_str) → must be 0-255

// 5. Parse verb (between colons)
verb_end = find ':' after colon+1, or body_len
verb_len = verb_end - colon - 1 (1-16 chars, alnum/underscore)
copy to out->verb

// 6. Parse fields (if verb_end < body_len)
fields_len = body_len - verb_end - 1 (max 64 chars)
copy to out->fields

// 7. Set seq
out->seq = (uint8_t)seq;
return 0;
```

---

## CRC16 Implementation (`crc16.c`)

### `uint16_t vaanicore_crc16(const uint8_t *data, size_t length)`
Standard CRC-16/CCITT-FALSE:
- Polynomial: 0x1021
- Initial value: 0xFFFF
- No reflection
- No final XOR

```c
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
```

---

## Test Vectors (`tests/protocol/vectors.json`)

```json
[
  {"frame": "@1:PINGECA9\n", "seq": 1, "verb": "PING", "fields": {}},
  {"frame": "@2:RUN_SIMULATION:project=amplifierDDCD\n", "seq": 2, "verb": "RUN_SIMULATION", "fields": {"project": "amplifier"}}
]
```

---

## Invariants

1. **No heap allocation** — All buffers stack/static, capacity passed in
2. **Bounded output** — Capacity checked at each snprintf
3. **Max frame 128 bytes** — Enforced in encode (body≤123, total≤128) and decode
4. **CRC on every frame** — Encode always adds, decode always verifies
5. **Python parity** — Same inputs produce identical frames
6. **Error codes distinct** — -1=format, -2=CRC, 0=success
7. **Seq modulo 256** — uint8_t, wraps automatically
8. **Field validation** — Verb: alnum/underscore; Fields: key=[a-z][a-z0-9_]*, no commas in values

---

## Test Coverage

| Test | Verifies |
|------|----------|
| `make protocol-test` | C encode/decode matches vectors |
| `test_crc_known_vector` | CRC matches known values |
| `test_round_trip` | Python encode → C decode → Python encode |
| `test_shared_vectors` | Python/C vectors identical |
| `test_corruption_rejected` | Bit flips detected |
| `test_oversize_rejected` | >128 bytes rejected |

---

## Failure Modes

| Condition | Encode Return | Decode Return |
|-----------|---------------|---------------|
| NULL verb/out | -1 | -1 |
| Capacity too small | -1 | -1 |
| Body > 123 chars | -1 | -1 |
| Total > capacity | -1 | -1 |
| Invalid frame format | N/A | -1 |
| CRC mismatch | N/A | -2 |
| Seq > 255 | N/A | -1 |
| Invalid verb chars | N/A | -1 |
| Invalid field format | N/A | -1 |

---

## Acceptance Criteria

- Encode/decode API specified with exact behavior
- Data structures defined with bounds
- CRC16 algorithm specified
- Test vectors documented
- 8 invariants enumerated
- Failure modes table complete
- Test coverage mapped
- Next step (0234) can use this output