DOCKER := "$(shell { command -v podman || command -v docker; })"
TIMESTAMP := "$(shell date -u +"%Y%m%d%H%M")"
COMMIT := "$(shell git rev-parse --short HEAD 2>/dev/null)"
detected_OS := "$(shell uname)"  # Classify UNIX OS
ifeq ($(strip $(detected_OS)),Darwin) #We only care if it's OS X
SELINUX1 :=
SELINUX2 :=
else
SELINUX1 := :z
SELINUX2 := ,z
endif

.PHONY: all clean

all:
	$(shell bin/get_version.sh >> /dev/null)
	$(DOCKER) build --tag zmk --file Dockerfile .
	$(DOCKER) run --rm -it --name zmk \
		-v $(PWD)/firmware:/app/firmware$(SELINUX1) \
		-v $(PWD)/config:/app/config:ro$(SELINUX2) \
		-e TIMESTAMP=$(TIMESTAMP) \
		-e COMMIT=$(COMMIT) \
		zmk

clean:
	rm -f firmware/*.uf2
	$(DOCKER) image rm zmk docker.io/zmkfirmware/zmk-build-arm:stable
