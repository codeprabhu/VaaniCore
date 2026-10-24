# Transport walkthrough

`host/transport.py` keeps serial access optional: `--stdio` supports virtual/CI operation, while `--port` uses pyserial with a bounded line read and optional VID/description discovery. Open/read/write disconnects enter a reconnect loop and resend the connection handshake. The handler always decodes and validates a frame before dispatching it; no raw device text is passed to a shell.

Viva questions: Why line reads? The protocol is newline framed. What happens without pyserial? The agent reports a clear dependency error. Why filter ports? Avoid acting on unrelated serial devices. What bounds a frame? The codec rejects frames over 128 bytes. How is CI independent of hardware? It uses `--stdio` or the virtual device.
