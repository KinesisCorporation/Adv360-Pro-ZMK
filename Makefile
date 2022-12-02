DOCKER := $(shell { command -v podman || command -v docker; })
TIMESTAMP := $(shell date -u +"%Y%m%d%H%M%S")

.PHONY: all clean

all:
	$(DOCKER) build --tag zmk --file Dockerfile .
	$(DOCKER) run --rm -it --name zmk \
		-v $(PWD)/firmware:/app/firmware:z \
		-v $(PWD)/config:/app/config:ro,z \
		-e TIMESTAMP=$(TIMESTAMP) \
		zmk

clean:
	rm -f firmware/*.uf2
	$(DOCKER) image rm zmk docker.io/zmkfirmware/zmk-build-arm:stable
