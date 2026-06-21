# Root Makefile — delegates to pipeline/
.PHONY: setup data data-synthetic ingest qc infer metrics export figures validate test check

%:
	$(MAKE) -C pipeline $@

check:
	./scripts/check-portfolio.sh
