"""Audit Phase-A repository state without upgrading scaffolds into claims."""
from __future__ import annotations
import argparse, json, pathlib, shutil, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.provenance import generated_provenance

def main() -> None:
    parser = argparse.ArgumentParser(description="Audit VaaniCore Phase-A evidence state")
    parser.add_argument("--output", default="results/phase_a_audit.json")
    args = parser.parse_args()
    required = ["Makefile", "host/protocol.py", "host/host_agent.py", "firmware/main/pins.h", "ml/features.py", "deck/build_deck.py", "results/summary.json"]
    placeholders = []
    for path in ROOT.rglob("*"):
        if path.is_file() and ".git" not in path.parts and path.suffix in {".md", ".csv", ".yaml", ".py"}:
            if "[[HUMAN" in path.read_text(errors="ignore"):
                placeholders.append(str(path.relative_to(ROOT)))
    data = {"provenance": generated_provenance({"required_count": len(required)}), "label": "AUDIT", "checks": {
        "required_files": {"status": "PASS" if all((ROOT / path).is_file() for path in required) else "FAIL", "missing": [path for path in required if not (ROOT / path).is_file()]},
        "official_template": {"status": "PRESENT" if (ROOT / "inputs/Vishwakarma_Awards_2026-27_Stage_2_Submission_Template.pptx").is_file() else "MISSING"},
        "idea_pdf": {"status": "PRESENT" if (ROOT / "inputs/vishwakarma.pdf").is_file() else "MISSING"},
        "idf": {"status": "AVAILABLE" if shutil.which("idf.py") else "UNAVAILABLE"},
        "ngspice": {"status": "AVAILABLE" if shutil.which("ngspice") else "UNAVAILABLE"},
        "python_pptx": {"status": "AVAILABLE" if _python_pptx_available() else "UNAVAILABLE"},
        "intentional_human_placeholders": {"status": "PRESENT" if placeholders else "NONE", "files": placeholders},
        "simulated_summary": {"status": "EXPLICITLY_LABELLED", "path": "results/summary.json"}
    }}
    output = ROOT / args.output; output.parent.mkdir(parents=True, exist_ok=True); output.write_text(json.dumps(data, indent=2) + "\n"); print(output)

def _python_pptx_available() -> bool:
    try:
        import pptx  # noqa: F401
        return True
    except ImportError:
        return False

if __name__ == "__main__": main()
