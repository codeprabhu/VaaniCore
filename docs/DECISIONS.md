# Decisions

| Date | Decision | Alternatives | Reason |
|---|---|---|---|
| 2026-10-24 | Use `/home/shrivathssp/Desktop` as repository root | wait for a separate repo | Current workspace is not a Git checkout. |
| 2026-10-24 | Python 3.11-compatible standard-library protocol core first | hardware-first | Enables an auditable vertical slice without hardware. |
| 2026-10-24 | ESP-IDF target is v5.x; exact patch version remains `[[HUMAN: pin after toolchain install]]` | Arduino core | Required RTOS, GDMA and TinyUSB architecture. |
| 2026-10-24 | PTT is the Day-14 wake path; wake word is SHOULD | custom wake word first | Protects the demo deadline. |
| 2026-10-24 | Generate the draft deck by editing template OOXML directly | wait for unavailable python-pptx | Keeps the supplied theme/assets and produces a valid 18-slide PPTX in this sandbox. Visual rendering remains a tool limitation and requires human QA in PowerPoint/LibreOffice. |
| 2026-10-24 | Keep optional larger AI/cloud layer out of the Day-14 dependency graph | make cloud interpretation primary | Matches the idea document and preserves offline operation, privacy, and measurable partitioning. |
