# define name of virtual environment directory
VENV := venv

my_debug:
	@echo "==== $(OS) ===="

# differnt procedure for Windows and other OS
ifeq ($(OS),Windows_NT)
	py.exe -m venv $(VENV)
	./$(VENV)/Scripts/python.exe -m pip install .
else
	python3 -m venv $(VENV)
	./$(VENV)/bin/pip install .
endif

docs:
	pdoc3 src -o docs --html

.PHONY: all docs clean

tests:
	pdoc3 src -o docs --html

.PHONY: all tests clean

#run: venv
#	./$(VENV)/bin/python3 todo.py

clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete
	rm -rf docs/*

.PHONY: all venv run clean
