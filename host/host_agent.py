"""Safe host-side action dispatcher for VaaniCore's virtual and serial transports."""
from __future__ import annotations
import argparse, json, os, pathlib, shutil, subprocess, sys, time
from host.protocol import Frame, encode, decode
from host.measurements import parse_meas
from host.transport import discover_port, serve_serial

ALLOWED = {"PING", "OPEN_PROJECT", "RUN_SIMULATION", "SHOW_RESULT", "CLOSE_PROJECT"}
RISKY = {"CLOSE_PROJECT"}
ROOT = pathlib.Path(__file__).resolve().parents[1]
PROJECTS = {"amplifier": ROOT / "projects/amplifier", "filter": ROOT / "projects/filter", "regulator": ROOT / "projects/regulator"}

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
            if virtual:
                return Frame(frame.seq, "DONE", {"status": "ok", "project": project.name, "gain_db": "TARGET", "bw_hz": "TARGET", "label": "SIMULATED"})
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
        return Frame(frame.seq, "DONE", {"status": "ok", "project": project.name})
    return Frame(frame.seq, "DONE", {"status": "ok"})

def main() -> int:
    parser = argparse.ArgumentParser(description="VaaniCore allow-listed host agent")
    parser.add_argument("--stdio", action="store_true", help="read newline-delimited frames from stdin")
    parser.add_argument("--port", help="USB serial port; auto-detection is used if omitted")
    parser.add_argument("--baud", type=int, default=115200)
    args = parser.parse_args()
    def handler(line: bytes) -> bytes:
        try:
            return encode(dispatch(decode(line)))
        except Exception as exc:
            return encode(Frame(0, "ERR", {"code": type(exc).__name__}))
    if args.stdio:
        for line in sys.stdin.buffer:
            sys.stdout.buffer.write(handler(line)); sys.stdout.buffer.flush()
    else:
        port = args.port or discover_port()
        if not port:
            raise SystemExit("no VaaniCore serial port found; provide --port or use --stdio")
        serve_serial(port, handler, args.baud)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
