# Protocol walkthrough

`host/protocol.py` owns CRC-16/CCITT-FALSE framing. `encode` sorts fields for deterministic bytes; `decode` validates length, newline, hexadecimal CRC, body syntax, and key syntax before returning a typed frame.

Viva questions: Why CRC? To detect corruption. Why newline? Human debugging and stream framing. Why sorted fields? Stable vectors. Why max 128 bytes? Bounded buffering. What is retried? The transport layer retries a sequence after 300 ms, up to three times.
