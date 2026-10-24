.PHONY: test sim-demo bench audit hardware-check cad-check intent-test deck-draft deck-final phase-a
PYTHON ?= python3

test: protocol-test context-test dsp-test intent-test
	PYTHONPATH=. $(PYTHON) -m unittest discover -s tests -p 'test_*.py' -v

sim-demo:
	PYTHONPATH=. $(PYTHON) -m host.tools.virtual_device --project amplifier
	PYTHONPATH=. $(PYTHON) host/tools/stdio_demo.py

bench:
	PYTHONPATH=. $(PYTHON) bench/run_benchmarks.py
	PYTHONPATH=. $(PYTHON) bench/validate_summary.py
	PYTHONPATH=. $(PYTHON) bench/analyze.py --figures
	PYTHONPATH=. $(PYTHON) bench/analyze_timing.py

smoke:
	PYTHONPATH=. $(PYTHON) ml/smoke_test.py

audit:
	PYTHONPATH=. $(PYTHON) tools/audit_phase_a.py
	PYTHONPATH=. $(PYTHON) tools/validate_fmea.py

hardware-check:
	PYTHONPATH=. $(PYTHON) hardware/validate_pinmap.py
	PYTHONPATH=. $(PYTHON) hardware/power_budget.py

cad-check:
	PYTHONPATH=. $(PYTHON) hardware/cad/analytical_checks.py
	PYTHONPATH=. $(PYTHON) hardware/cad/enclosure.py --help

dsp-test:
	$(CC) -std=c11 -O2 -Ifirmware/components/dsp tests/dsp_parity.c firmware/components/dsp/mfcc.c -lm -o /tmp/vaanicore_dsp_test
	/tmp/vaanicore_dsp_test

protocol-test:
	$(CC) -std=c11 -O2 -Ifirmware/components/protocol tests/protocol_c.c firmware/components/protocol/protocol.c firmware/components/protocol/crc16.c -o /tmp/vaanicore_protocol_test
	/tmp/vaanicore_protocol_test

context-test:
	$(CC) -std=c11 -O2 -Ifirmware/components/context tests/context_c.c firmware/components/context/context.c -o /tmp/vaanicore_context_test
	/tmp/vaanicore_context_test

intent-test:
	$(CC) -std=c11 -O2 -Ifirmware/main tests/intents_c.c firmware/main/intents.c -o /tmp/vaanicore_intent_test
	/tmp/vaanicore_intent_test

deck-draft:
	PYTHONPATH=. $(PYTHON) deck/build_deck.py --draft

figures:
	$(PYTHON) deck/figures/generate_figures.py

deck-final:
	PYTHONPATH=. $(PYTHON) deck/build_deck.py --final

phase-a:
	$(MAKE) test
	$(MAKE) sim-demo
	$(MAKE) bench
	$(MAKE) audit
	$(MAKE) hardware-check
	$(MAKE) cad-check
	$(MAKE) deck-draft
