# ADV360-PRO-ZMK

## To build Firmware in GitHub Actions

### Setup

1. Fork this repo.
2. Enable GitHub Actions on your fork.

### Build firmware

1. Push a commit to trigger the build.
2. Download the artifact.

## To build Firmware locally using a container

### First run

Note: Either Podman or Docker is required, Podman is preferred if both are present.

1. Execute `make all`.
2. Check the `firmware` directory for the latest firmware build.

### Subsequent runs

If the only file you have changed is `config/adv360.keymap`, execute `make build` and check the `firmware` directory for the latest firmware build.

If you have changed other files in the `config` directory (such as `config/west.yml`) you will need to execute `make all` to rebuild the Docker image as well as the firmware.

### Flash firmware

Resources can be found on Kinesis.com
https://kinesis-ergo.com/support/kb360pro/#firmware-updates
https://kinesis-ergo.com/support/kb360pro/#manuals
