# Production simulation demo — one command for the full Dino workflow
#
#   make demo
#
# Requires: Python 3.10+, dino installed editable (pip install -e ".[dev]")

ROOT := $(abspath ../..)
ifndef PY
  ifneq ($(wildcard $(ROOT)/.venv/bin/python),)
    PY := $(ROOT)/.venv/bin/python
  else
    PY := python3
  endif
endif
export DINO_EA_SIGNING_SECRET ?= dino-demo-makefile
export PYTHONPATH := $(ROOT)

WORK := $(CURDIR)/_work
ARCHIVE := $(WORK)/archive
GOLDEN := $(CURDIR)/golden

.PHONY: demo clean golden-update

demo: clean
	@mkdir -p $(WORK)/v1 $(WORK)/v2 $(ARCHIVE)
	@$(PY) -c "from dino.license import DEFAULT_LICENSE, activate_pack, save_license; \
	  import dino.license as L, os, tempfile; \
	  from pathlib import Path; \
	  from dino.early_access import issue_key; \
	  d=Path('$(WORK)')/'.dino'; d.mkdir(parents=True, exist_ok=True); \
	  L.LICENSE_DIR=d; L.LICENSE_PATH=d/'license.json'; \
	  save_license(dict(DEFAULT_LICENSE)); \
	  activate_pack('proof', key=issue_key(team='demo', days=30))"
	@DINO_LICENSE_DIR="$(WORK)/.dino" $(PY) $(CURDIR)/scripts/run_demo.py \
		--python $(PY) \
		--pipeline $(CURDIR)/pipeline \
		--work $(WORK) \
		--archive $(ARCHIVE) \
		--golden $(GOLDEN)
	@echo ""
	@echo "Demo complete. Artifacts: $(ARCHIVE)"
	@echo "Compare your proof_index.json to golden/ (deterministic schemas)."

golden-update:
	@$(PY) $(CURDIR)/scripts/run_demo.py \
		--python $(PY) \
		--pipeline $(CURDIR)/pipeline \
		--work $(WORK) \
		--archive $(ARCHIVE) \
		--golden $(GOLDEN) \
		--write-golden

clean:
	@rm -rf $(WORK)
