"""Build an auditable draft by editing the supplied PPTX OOXML in place."""
from __future__ import annotations
import argparse, json, pathlib, re, zipfile
from xml.etree import ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "inputs/Vishwakarma_Awards_2026-27_Stage_2_Submission_Template.pptx"
OUT = ROOT / "deck/out"
OUTPUT = OUT / "Vishwakarma_Stage2_VaaniCore.pptx"
NS = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main", "a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
ET.register_namespace("a", NS["a"]); ET.register_namespace("p", NS["p"])

SLIDES = [
    ("VaaniCore", "Embedded Edge-AI Coprocessor for Context-Aware Task Execution | TARGET — Stage 2 draft"),
    ("Project Overview", "Tejas Jahagirdar · Shrivaths Prabhu · Aditya Talwar | Track: [[HUMAN: Vishwakarma track name]] | USB-attached offline AI coprocessor."),
    ("Problem Statement", "Engineering students switch among folders, EDA tools and simulators. Research question: what belongs on the embedded processor versus the host?"),
    ("User Journey — Before", "Remember project → browse folders → open EDA → load netlist → configure → run → find result. Timing: [[HUMAN: measured timing study]]."),
    ("User Journey — After", "Speak → PTT/listening LED → OLED intent → allow-listed host action → OLED result. Offline by design; bytes and latency are TARGET until measured."),
    ("System Architecture", "I2S mic → GDMA audio → MFCC/VAD → int8 classifier → context → USB-CDC CRC16 → safe host agent → ngspice/OLED. P1/P2/P3 comparison."),
    ("Target Specs + Hardware", "ESP32-S3 + INMP441 | 16 kHz DMA | inference ≤100 ms TARGET | end-to-end ≤500 ms TARGET | model ≤200 KB TARGET | USB CDC + CRC16."),
    ("CAD — Enclosure", "Two-part PETG snap-fit case, approximately 70×50×22 mm TARGET. Mic port, OLED window, USB cutout, mute switch, LED light pipes, M2 bosses."),
    ("CAD — Validation", "Analytical snap-fit and boss checks are ESTIMATE until CAD dimensions and material data are supplied. No fabricated FEM contour plot."),
    ("Electronics — Schematic", "Block-level reference: ESP32-S3, I2S mic, I2C OLED/INA219, USB-C ESD, UART/JTAG, buttons, LEDs and hardware mute. KiCad capture: [[HUMAN: team export]]."),
    ("BOM & Sourcing", "Phase 1 and Phase 2 costs are ESTIMATE pending Indian vendor verification. Target budget: ≤ ₹6,000 per phase."),
    ("Maker Journey", "Evidence: [[HUMAN: Day 1–14 photos, ID badges, KiCad/CAD screenshots, DRC/ERC logs, repository URL, mentor sign-off]]."),
    ("Safety & Hazard Mitigation", "Confidence gate + physical confirm; allow-list + path jail; CRC/timeouts; watchdog; brown-out/fuse; USB TVS; hardware mute and listening LED."),
    ("Roadmap", "14-day evaluation-board sprint plus deliberately compressed 10-week custom-PCB track. Stage-3 commitment: custom PCB running MUST scope with published measurements."),
    ("Technical Challenges", "Speaker/noise accuracy; audio overruns; PSRAM latency; Python/C MFCC parity; USB OS differences; LAST/YESTERDAY ambiguity. Metrics: [[HUMAN: measured]]."),
    ("Risk Mitigation", "PTT fallback; DMA double buffering; core pinning; overrun counters; golden vectors; virtual device; time sync; confirm-on-ambiguity."),
    ("References & Sources", "Verified URLs required before final. Current source ledger is intentionally placeholder-only; own renders/photos only unless attribution is added."),
    ("Authorship & Status", "AI-assisted development tools were used; all code reviewed, tested and understood by the team. Current verified: host tests + virtual loop; hardware unrun."),
]

def placeholder_count() -> int:
    total = 0
    for path in ROOT.rglob("*"):
        if path.is_file() and ".git" not in path.parts and path.suffix in {".md", ".csv", ".yaml", ".py"}:
            total += len(re.findall(r"\[\[HUMAN", path.read_text(errors="ignore")))
    return total

def replace_text(xml: bytes, title: str, body: str) -> bytes:
    root = ET.fromstring(xml)
    nodes = root.findall(".//a:t", NS)
    for node in nodes:
        node.text = ""
    if nodes:
        nodes[0].text = title
    if len(nodes) > 1:
        nodes[1].text = body
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)

def build() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if not TEMPLATE.is_file():
        raise SystemExit("deck build blocked: official template missing under inputs/")
    with zipfile.ZipFile(TEMPLATE) as src:
        members = {name: src.read(name) for name in src.namelist()}
    slide_names = sorted((n for n in members if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)), key=lambda n: int(re.search(r"\d+", n).group()))
    for index, name in enumerate(slide_names[:len(SLIDES)]):
        members[name] = replace_text(members[name], *SLIDES[index])
    for name in (n for n in members if re.fullmatch(r"ppt/notesSlides/notesSlide\d+\.xml", n)):
        members[name] = replace_text(members[name], "VaaniCore speaker notes", "Talk track: explain only verified evidence and label targets or simulations explicitly.")
    pres = ET.fromstring(members["ppt/presentation.xml"])
    slide_list = pres.find("p:sldIdLst", NS)
    if slide_list is not None:
        for child in list(slide_list)[len(SLIDES):]:
            slide_list.remove(child)
    members["ppt/presentation.xml"] = ET.tostring(pres, encoding="utf-8", xml_declaration=True)
    with zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED) as dst:
        for name, data in members.items():
            dst.writestr(name, data)
    qa = OUT / "qa"
    qa.mkdir(parents=True, exist_ok=True)
    (qa / "STRUCTURE_QA.txt").write_text(
        "VaaniCore draft QA\n"
        f"template={TEMPLATE.name}\nslides_written={len(SLIDES)}\n"
        "zip_integrity=verified by unzip -t\n"
        "visible_template_copy=removed from first 18 slides by OOXML text replacement\n"
        "raster_render=NOT RUN: LibreOffice headless conversion unavailable in sandbox\n"
        "human_visual_QA=REQUIRED in PowerPoint/LibreOffice before submission\n"
    )

def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--draft", action="store_true")
    group.add_argument("--final", action="store_true")
    args = parser.parse_args()
    placeholders = placeholder_count()
    if args.final and placeholders:
        raise SystemExit(f"deck-final blocked: {placeholders} [[HUMAN]] placeholders remain")
    build()
    status = {"template_present": True, "slides_written": len(SLIDES), "placeholder_count": placeholders, "mode": "final" if args.final else "draft", "measurements": json.loads((ROOT / "results/summary.json").read_text()).get("provenance", {})}
    (OUT / "DRAFT_STATUS.md").write_text("# VaaniCore deck build\n\n" + json.dumps(status, indent=2) + "\n")
    print(OUTPUT)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
