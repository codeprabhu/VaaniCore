"""Safe host-side action dispatcher for VaaniCore's virtual and serial transports."""
from __future__ import annotations
import argparse, json, os, pathlib, re, shutil, subprocess, sys, time
ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from host.protocol import Frame, encode, decode
from host.measurements import parse_meas
from host.transport import discover_port, serve_serial
from host.session import HostSession
from host.audit_log import append_frame
from host.launcher import launch_project

ALLOWED = {"PING", "OPEN_PROJECT", "RUN_SIMULATION", "SHOW_RESULT", "CLOSE_PROJECT"}
RISKY = {"CLOSE_PROJECT"}
PROJECTS = {"amplifier": ROOT / "projects/amplifier", "filter": ROOT / "projects/filter", "regulator": ROOT / "projects/regulator"}


def _protocol_nack(raw: bytes, error: Exception) -> Frame:
    """Build a bounded NACK while recovering only a decimal sequence prefix."""
    match = re.match(rb"^@([0-9]{1,3}):", raw)
    seq = int(match.group(1)) % 256 if match else 0
    reason = "crc" if "CRC" in str(error).upper() else "malformed"
    return Frame(seq, "NACK", {"reason": reason})

def _project(name: str) -> pathlib.Path:
    if name not in PROJECTS or pathlib.Path(name).name != name:
        raise ValueError("unknown project id")
    path = PROJECTS[name].resolve()
    if ROOT not in path.parents:
        raise ValueError("project escapes root")
    return path

def dispatch(frame: Frame, confirm: bool = False, virtual: bool = False) -> Frame:
    if frame.verb not in ALLOWED:
        return Frame(frame.seq, "ERR", {"code": "verb_not_allowed"})
    if frame.verb in RISKY and not confirm:
        return Frame(frame.seq, "ERR", {"code": "physical_confirm_required"})
    if frame.verb == "PING":
        return Frame(frame.seq, "DONE", {"status": "ok"})
    if frame.verb in {"OPEN_PROJECT", "RUN_SIMULATION"}:
        try:
            project = _project(frame.fields.get("project", ""))
        except ValueError:
            return Frame(frame.seq, "ERR", {"code": "invalid_project_id"})
        if frame.verb == "RUN_SIMULATION":
            netlist = project / f"{project.name}.cir"
            if not netlist.is_file():
                return Frame(frame.seq, "ERR", {"code": "netlist_missing"})
            opened = False
            if frame.fields.get("open") == "1":
                try:
                    launch_project(project, dry_run=virtual)
                    opened = True
                except RuntimeError:
                    return Frame(frame.seq, "ERR", {"code": "opener_unavailable"})
            if virtual:
                fields = {"status": "ok", "project": project.name, "gain_db": "TARGET", "bw_hz": "TARGET", "label": "SIMULATED"}
                if opened:
                    fields["opened"] = "1"
                return Frame(frame.seq, "DONE", fields)
            if not shutil.which("ngspice"):
                return Frame(frame.seq, "ERR", {"code": "ngspice_unavailable"})
            log = project / "results.log"
            completed = subprocess.run(["ngspice", "-b", "-o", str(log), str(netlist)], cwd=project, check=False, capture_output=True, text=True)
            if completed.returncode != 0:
                return Frame(frame.seq, "ERR", {"code": "simulation_failed"})
            values = parse_meas(log.read_text(errors="replace")) if log.is_file() else {}
            fields = {"status": "ok", "project": project.name, "label": "MEASURED"}
            for key in ("gain_db", "bw_hz"):
                if key in values:
                    fields[key] = str(values[key])
            return Frame(frame.seq, "DONE", fields)
        try:
            opener = launch_project(project, dry_run=virtual)
        except RuntimeError:
            return Frame(frame.seq, "ERR", {"code": "opener_unavailable"})
        return Frame(frame.seq, "DONE", {"status": "ok", "project": project.name, "opener": opener, "label": "SIMULATED" if virtual else "MEASURED"})
    return Frame(frame.seq, "DONE", {"status": "ok"})

def main() -> int:
    parser = argparse.ArgumentParser(description="VaaniCore allow-listed host agent")
    parser.add_argument("--stdio", action="store_true", help="read newline-delimited frames from stdin")
    parser.add_argument("--port", help="USB serial port; auto-detection is used if omitted")
    parser.add_argument("--baud", type=int, default=115200)
    parser.add_argument("--log", default="logs/host_agent.jsonl", help="JSONL audit log path")
    parser.add_argument("--virtual", action="store_true", help="use simulated project actions; CI/demo only")
    args = parser.parse_args()
    session = HostSession(virtual=args.virtual)
    def handler(line: bytes) -> bytes:
        try:
            request = decode(line)
            append_frame(args.log, "device_to_host", request)
            responses = session.handle(request)
            for response in responses:
                append_frame(args.log, "host_to_device", response)
            return b"".join(encode(frame) for frame in responses)
        except ValueError as exc:
            nack = _protocol_nack(line, exc)
            append_frame(args.log, "host_to_device", nack, str(exc))
            return encode(nack)
        except Exception as exc:
            append_frame(args.log, "host_error", Frame(0, "ERR", {"code": type(exc).__name__}), str(exc))
            return encode(Frame(0, "ERR", {"code": type(exc).__name__}))
    if args.stdio:
        for line in sys.stdin.buffer:
            sys.stdout.buffer.write(handler(line)); sys.stdout.buffer.flush()
    else:
        port = args.port or discover_port()
        if not port:
            raise SystemExit("no VaaniCore serial port found; provide --port or use --stdio")
        # Send TIME_SYNC immediately after opening the serial link, then process requests.
        def connected_handler(line: bytes) -> bytes:
            return handler(line)
        serve_serial(port, connected_handler, args.baud, on_connect=lambda: b"".join(encode(frame) for frame in session.connect_frames()))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
