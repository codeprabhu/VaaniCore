"""Platform-specific fixed-argv project launcher; never uses a shell."""
from __future__ import annotations
import os, pathlib, shutil, sys

def open_command(project: pathlib.Path, platform_name: str | None = None) -> list[str] | None:
    platform_name = platform_name or sys.platform
    path = str(project.resolve())
    if platform_name.startswith("win"):
        return None  # caller uses os.startfile, which has no argv form.
    if platform_name == "darwin":
        return ["open", path] if shutil.which("open") else None
    return ["xdg-open", path] if shutil.which("xdg-open") else None

def launch_project(project: pathlib.Path, dry_run: bool = False) -> str:
    command = open_command(project)
    if sys.platform.startswith("win"):
        if dry_run: return "os.startfile"
        os.startfile(str(project.resolve()))  # type: ignore[attr-defined]
        return "os.startfile"
    if not command:
        raise RuntimeError("platform opener unavailable")
    if dry_run:
        return " ".join(command)
    import subprocess
    subprocess.Popen(command, cwd=project, close_fds=True)
    return command[0]
