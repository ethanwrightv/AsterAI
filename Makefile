.PHONY: install test docs

install:
\tpip install -e src

test:
\tpython -m pytest

docs:
\t@echo "Review docs/usage.md and docs/roadmap.md before publishing."
