# VaaniCore protocol

Frames are ASCII, newline terminated, maximum 128 bytes:
`@<seq>:<VERB>[:k=v,k=v]*<CRC16-CCITT hex4>\n`

CRC is CRC-16/CCITT-FALSE, polynomial `0x1021`, initial value `0xffff`, calculated over the bytes from `@` through the final field before the four hex CRC digits. Sequence numbers are decimal modulo 256. Receivers reject malformed, oversized, or CRC-invalid frames and return `NACK` where a sequence can be recovered.

The Python implementation in `host/protocol.py` is the executable reference. The C implementation in
`firmware/components/protocol/` now provides both bounded encoding and decoding (`vaanicore_encode_frame` /
`vaanicore_decode_frame`) without heap allocation; C firmware must match it and use the vectors in
`tests/protocol/vectors.json`.

For a combined spoken request, `RUN_SIMULATION:project=amplifier,open=1` asks the host to perform the allow-listed
project launch before simulation. The response reports only the bounded flag `opened=1`; it never places a host path or
launcher command in the frame.

Reliability policy: sequence numbers, idempotent handling, retransmit after 300 ms up to three attempts, 30 s task timeout, CRC failure → NACK, and garbage/oversize frames dropped with counters. `host/reliability.py` is the executable bounded retry policy. Cross-device clock estimation error remains `[[HUMAN: measure on hardware]]`.
