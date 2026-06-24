PYTHON ?= python3

.PHONY: help status words build day1 day2 day3 day4 day5 day6 day7

help:
	@echo "Verfuegbare Befehle:"
	@echo "  make status   - Soll/Ist-Fortschritt anzeigen"
	@echo "  make words    - Wortzahl ueber alle Kapitel"
	@echo "  make build    - Finales Manuskript erzeugen"
	@echo "  make day1..day7 - Tagesziele anzeigen"

status:
	@$(PYTHON) tools/progress_report.py

words:
	@$(PYTHON) tools/word_count.py

build:
	@$(PYTHON) tools/build_manuscript.py

day1:
	@$(PYTHON) tools/day_goal.py 1

day2:
	@$(PYTHON) tools/day_goal.py 2

day3:
	@$(PYTHON) tools/day_goal.py 3

day4:
	@$(PYTHON) tools/day_goal.py 4

day5:
	@$(PYTHON) tools/day_goal.py 5

day6:
	@$(PYTHON) tools/day_goal.py 6

day7:
	@$(PYTHON) tools/day_goal.py 7
