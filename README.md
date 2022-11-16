# ADV360-PRO-ZMK

## To build Firmware in GitHub Actions

### Setup

1. Fork this repo.
2. Enable GitHub Actions on your fork.

### Build firmware

1. Push a commit to trigger the build.
2. Download the artifact.

## To build Firmware locally using a container

Note: Either Podman or Docker is required, Podman is preferred if both are present.
If compiling on Windows use WSL2 and docker [Docker Setup Guide](https://docs.docker.com/desktop/windows/wsl/).

1. Execute `make`.
2. Check the `firmware` directory for the latest firmware build.
3. Follow the programming instruction on page 8 of the [Quick Start Guide](https://kinesis-ergo.com/wp-content/uploads/Advantage360-Professional-QSG-v8-25-22.pdf) to flash the firmware.

### Cleanup

The built docker container and compiled firmware files can be deleted with `make clean`.

### Flash firmware

Resources can be found on Kinesis.com
https://kinesis-ergo.com/support/kb360pro/#firmware-updates
https://kinesis-ergo.com/support/kb360pro/#manuals
