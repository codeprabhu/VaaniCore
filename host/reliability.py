"""Transport-independent bounded retry policy for VaaniCore frames."""
from __future__ import annotations
from collections.abc import Callable
from host.protocol import Frame, decode, encode

SendAndReceive = Callable[[bytes, float], bytes | None]

def request_with_retries(request: Frame, send_and_receive: SendAndReceive, attempts: int = 3, timeout_s: float = 0.300) -> Frame:
    if attempts < 1 or attempts > 3:
        raise ValueError("attempts must be between 1 and 3")
    last_error: Exception | None = None
    for _ in range(attempts):
        try:
            raw = send_and_receive(encode(request), timeout_s)
            if not raw:
                raise TimeoutError("no response")
            response = decode(raw)
            if response.verb == "NACK":
                raise RuntimeError(response.fields.get("reason", "NACK"))
            return response
        except (TimeoutError, RuntimeError, ValueError) as exc:
            last_error = exc
    raise TimeoutError(f"request failed after {attempts} attempts: {last_error}")
