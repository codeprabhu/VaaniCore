# VaaniCore protocol

Frames are ASCII, newline terminated, maximum 128 bytes:
`@<seq>:<VERB>[:k=v,k=v]*<CRC16-CCITT hex4>\n`

CRC is CRC-16/CCITT-FALSE, polynomial `0x1021`, initial value `0xffff`, calculated over the bytes from `@` through the final field before the four hex CRC digits. Sequence numbers are decimal modulo 256. Receivers reject malformed, oversized, or CRC-invalid frames and return `NACK` where a sequence can be recovered.

The Python implementation in `host/protocol.py` is the executable reference. C firmware must match it and use the vectors in `tests/protocol/vectors.json`.
