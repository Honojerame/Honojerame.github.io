PYTHON ?= python3
.PHONY: all test cpu systolic memory noc lint synth report clean
all: test
test: cpu systolic memory noc
cpu:
	$(PYTHON) tools/test_cpu.py
systolic:
	$(PYTHON) tools/test_systolic.py
memory:
	$(PYTHON) tools/test_memory.py
noc:
	$(PYTHON) tools/test_noc.py
lint:
	$(PYTHON) tools/check_rtl.py lint
synth:
	$(PYTHON) tools/check_rtl.py synth
report:
	$(PYTHON) tools/report.py
clean:
	$(PYTHON) -c "import shutil; shutil.rmtree('build', ignore_errors=True)"
