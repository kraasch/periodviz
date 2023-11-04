
SHELL=/bin/bash

run:
	make clean
	make build
	make view

build:
	mkdir -p ./export/
	python3 src/periodviz.py -i 'example_data.csv' -o 'export/period.png' -t 2023

clean:
	rm -f ./export/*

view:
	sxiv ./export/period.png

hub_update:
	@hub_ctrl ${HUB_MODE} ln "$(realpath ./src/periodviz.py)" "${HOME}/.local/bin/periodviz"
