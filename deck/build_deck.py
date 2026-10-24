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
    ("References & Sources", "Verified primary-source ledger: ESP-IDF, esp-tflite-micro, ESP-DSP, TinyUSB, TFLM, device datasheets, ngspice, KiCad, CadQuery, datasets and local-ASR baselines."),
    ("Authorship & Status", "AI-assisted development tools were used; all code reviewed, tested and understood by the team. Current verified: host tests + virtual loop; hardware unrun."),
]

DETAILS = {
    1: ["Application ID: [[HUMAN: Vishwakarma Application ID]]", "Institution: [[HUMAN: institution]]", "Track: [[HUMAN: track]]", "Faculty mentor: [[HUMAN: mentor]]"],
    2: ["Core innovation", "Offline local processing", "Measured local-versus-host partitioning", "Allow-listed desktop actions"],
    3: ["Beneficiary: electronics and embedded engineering students", "Multi-tool workflow", "Context is hard to recall", "Cloud adds connectivity/privacy cost", "Question: what belongs on edge versus host?"],
    4: ["1 Remember project", "2 Browse folders", "3 Open EDA", "4 Configure", "5 Run", "6 Find result", "Time/actions: [[HUMAN: timing study]]"],
    5: ["1 Speak", "2 LED listening", "3 OLED parsed intent", "4 Host action", "5 OLED result", "Offline: TARGET", "USB bytes: TARGET"],
    6: ["P1 Full-edge", "P2 Hybrid", "P3 Host-only", "I2S + GDMA", "MFCC + VAD + int8", "NVS context", "USB-CDC + CRC16", "Allow-listed host"],
    7: ["Audio: 16 kHz / 16-bit — TARGET", "Inference: ≤100 ms — TARGET", "End-to-end: ≤500 ms — TARGET", "Accuracy: ≥92% — TARGET", "Model: ≤200 KB / ≤120 KB — TARGET", "Power: ≤0.6 W — TARGET", "FreeRTOS dual-core + TWDT"],
    8: ["PETG case — TARGET", "Mic acoustic port", "OLED window", "USB-C cutout", "Mute switch", "LED light pipes", "4× M2 bosses"],
    9: ["PETG / PLA / ABS comparison: [[HUMAN: verify datasheets]]", "Snap strain: ESTIMATE", "Boss bending: ESTIMATE", "FEM: not run", "CAD export: [[HUMAN: team native files]]"],
    10: ["Power: USB-C → fuse → 3V3 LDO", "MCU: ESP32-S3", "Audio: INMP441 I2S", "Display/sense: OLED + INA219 I2C", "Safety: mute, buttons, LEDs", "Pin map: firmware/main/pins.h"],
    11: ["Phase 1 budget ≤ ₹6,000 — ESTIMATE", "Phase 2 budget ≤ ₹6,000 — ESTIMATE", "ESP32-S3 DevKit", "INMP441", "SSD1306", "INA219", "Vendor/lead time: [[HUMAN: verify]]"],
    12: ["Day evidence: [[HUMAN: photos]]", "KiCad: [[HUMAN: screenshots + ERC/DRC]]", "CAD: [[HUMAN: renders]]", "Repository: [[HUMAN: URL]]", "Authorship ledger maintained", "Mentor: [[HUMAN: sign-off]]"],
    13: ["Mis-recognition → confirm gate", "Injection → allow-list/path jail", "USB fault → CRC/timeout", "Hang → TWDT", "Brown-out → BOD/fuse", "ESD → USB TVS", "Privacy → mute/LED", "Thermal → LDO check"],
    14: ["Days 1–6: bring-up + virtual loop", "Days 7–11: context + measurements", "Days 12–14: CAD + deck + freeze", "Weeks 3–12: compressed custom PCB", "Stage 3: measured custom-PCB demo"],
    15: ["Accuracy across speakers/noise", "Audio overruns", "PSRAM latency", "Python/C parity", "USB OS differences", "Context ambiguity", "Observed metrics: [[HUMAN: measure]]"],
    16: ["PTT fallback", "Augmentation + speaker holdout", "DMA buffers + counters", "SRAM/PSRAM comparison", "Golden vectors", "Virtual device", "Time sync + confirm"],
    17: ["ESP-IDF / ESP32-S3 I2S + USB — verified", "esp-tflite-micro / ESP-DSP — verified", "TinyUSB CDC — verified", "INMP441 / INA219 datasheets — verified", "ngspice / KiCad / CadQuery — verified", "Speech Commands / Hello Edge / ESC-50 — verified", "Vosk / faster-whisper — baseline sources", "Own renders/photos only; attribution remains human check"],
    18: ["Verified software: protocol, context, MFCC, safety", "Simulated only: virtual trials", "Written, not built: ESP-IDF", "AI-assisted development tools were used; all code reviewed, tested and understood by the team.", "Final review: [[HUMAN: team sign-off]]"],
}

def placeholder_count() -> int:
    total = 0
    for path in ROOT.rglob("*"):
        if path.is_file() and ".git" not in path.parts and path.suffix in {".md", ".csv", ".yaml", ".py"}:
            total += len(re.findall(r"\[\[HUMAN", path.read_text(errors="ignore")))
    return total

def replace_text(xml: bytes, title: str, body: str, extras: list[str] | None = None) -> bytes:
    root = ET.fromstring(xml)
    nodes = root.findall(".//a:t", NS)
    for node in nodes:
        node.text = ""
    if nodes:
        nodes[0].text = title
    if len(nodes) > 1:
        nodes[1].text = body
    for node, value in zip(nodes[2:], extras or []):
        node.text = value
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)

def build(summary: dict) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if not TEMPLATE.is_file():
        raise SystemExit("deck build blocked: official template missing under inputs/")
    with zipfile.ZipFile(TEMPLATE) as src:
        members = {name: src.read(name) for name in src.namelist()}
    architecture_png = ROOT / "deck/assets/architecture.png"
    if architecture_png.is_file():
        # The official template's slide 6 rId3 is its full-slide architecture image.
        # Reusing that relationship preserves the template's visual structure.
        members["ppt/media/image11.png"] = architecture_png.read_bytes()
    slide_names = sorted((n for n in members if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)), key=lambda n: int(re.search(r"\d+", n).group()))
    slide_specs = list(SLIDES)
    provenance = summary.get("provenance", {})
    virtual_n = provenance.get("n", "unknown")
    virtual_label = provenance.get("label", "UNKNOWN")
    title, body = slide_specs[6]
    slide_specs[6] = (title, body + f" | Current benchmark source: {virtual_label}, N={virtual_n}; not a hardware measurement.")
    for index, name in enumerate(slide_names[:len(slide_specs)]):
        members[name] = replace_text(members[name], *slide_specs[index], DETAILS.get(index + 1, []))
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
    qa_result = _structural_qa(OUTPUT, len(slide_specs))
    qa = OUT / "qa"
    qa.mkdir(parents=True, exist_ok=True)
    (qa / "STRUCTURE_QA.txt").write_text(
        "VaaniCore draft QA\n"
        f"template={TEMPLATE.name}\nslides_written={len(slide_specs)}\n"
        f"zip_integrity={qa_result['zip_integrity']}\n"
        f"slide_count={qa_result['slide_count']}\n"
        f"forbidden_template_text={qa_result['forbidden_template_text']}\n"
        "visible_template_copy=removed from first 18 slides by OOXML text replacement\n"
        "raster_render=NOT RUN: LibreOffice headless conversion unavailable in sandbox\n"
        "human_visual_QA=REQUIRED in PowerPoint/LibreOffice before submission\n"
    )


def _structural_qa(path: pathlib.Path, expected_slides: int) -> dict[str, object]:
    """Verify archive and text invariants before reporting a draft as built."""
    with zipfile.ZipFile(path) as archive:
        bad_member = archive.testzip()
        all_slide_names = [
            name for name in archive.namelist()
            if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)
        ]
        presentation = ET.fromstring(archive.read("ppt/presentation.xml"))
        slide_list = presentation.find("p:sldIdLst", NS)
        active_count = len(list(slide_list)) if slide_list is not None else 0
        # This template's active slides are the first numbered slide parts;
        # unused example/instruction parts may remain as ZIP members.
        slide_names = sorted(all_slide_names, key=lambda name: int(re.search(r"\d+", name).group()))[:active_count]
        visible_text = "\n".join(
            archive.read(name).decode("utf-8", errors="ignore") for name in slide_names
        )
    forbidden = [term for term in ("Example:", "Instruction", "example project") if term in visible_text]
    result = {
        "zip_integrity": "PASS" if bad_member is None else f"FAIL:{bad_member}",
        "slide_count": active_count,
        "forbidden_template_text": "PASS" if not forbidden else ",".join(forbidden),
    }
    if bad_member is not None or active_count != expected_slides or forbidden:
        raise RuntimeError(f"deck structural QA failed: {result}")
    return result

def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--draft", action="store_true")
    group.add_argument("--final", action="store_true")
    args = parser.parse_args()
    placeholders = placeholder_count()
    if args.final and placeholders:
        raise SystemExit(f"deck-final blocked: {placeholders} [[HUMAN]] placeholders remain")
    summary = json.loads((ROOT / "results/summary.json").read_text())
    build(summary)
    status = {"template_present": True, "slides_written": len(SLIDES), "placeholder_count": placeholders, "mode": "final" if args.final else "draft", "measurements": summary.get("provenance", {})}
    (OUT / "DRAFT_STATUS.md").write_text("# VaaniCore deck build\n\n" + json.dumps(status, indent=2) + "\n")
    print(OUTPUT)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
