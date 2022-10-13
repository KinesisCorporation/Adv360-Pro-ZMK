TIMESTAMP := $(shell date -u +"%Y%m%d%H%M%S")

.PHONY: clean setup

all: setup build

build: firmware/$$(TIMESTAMP)-left.uf2 firmware/$$(TIMESTAMP)-right.uf2

clean:
	rm ./firmware/*.uf2

firmware/%-left.uf2 firmware/%-right.uf2: config/adv360.keymap
	docker run --rm -it --name zmk \
		-v $(PWD)/firmware:/app/firmware \
		-v $(PWD)/config:/app/config:ro \
		-e TIMESTAMP=$(TIMESTAMP) \
		zmk

setup: Dockerfile bin/build.sh config/west.yml
	docker build --tag zmk --file Dockerfile .
