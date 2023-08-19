# ADV360-PRO-ZMK

## Modifying the keymap

There is a GUI for editing the keymap. It is available at https://kinesiscorporation.github.io/Adv360-Pro-GUI

## Building the Firmware with GitHub Actions

### Setup

1. Fork this repo.
2. Enable GitHub Actions on your fork.

### Build firmware

1. Push a commit to trigger the build.
2. Download the artifact.

## Building the Firmware in a local container

### Setup

#### Software

* Either Podman or Docker is required, Podman is preferred if both are present.
* Make is also required

#### Windows specific

* If compiling on Windows use WSL2 and Docker [Docker Setup Guide](https://docs.docker.com/desktop/windows/wsl/).
* Install make using `sudo apt-get install make`.
* The repository can be cloned directly into the WSL2 instance or accessed through the C: mount point WSL provides by default (`/mnt/c/path-to-repo`).

### Build firmware

1. Execute `make`.
2. Check the `firmware` directory for the latest firmware build.

### Cleanup

The built docker container and compiled firmware files can be deleted with `make clean`.

## Flashing firmware

Follow the programming instruction on page 8 of the [Quick Start Guide](https://kinesis-ergo.com/wp-content/uploads/Advantage360-Professional-QSG-v8-25-22.pdf) to flash the firmware.

### briefly

1. Extract the firmwares from the downloaded archive.
1. Connect the left side keyboard to USB.
1. Press Mod+macro1 to put the left side into bootloader mode; it should attach to your computer as a USB drive.
1. Copy `left.uf2` to the USB drive and it will disconnect.
1. Power off both keyboards (by unplugging them and making sure the switches are off).
1. Turn on the left side keyboard with the switch.
1. Connect the right side keyboard to USB to power it on.
1. Press Mod+macro3 to put the right side into bootloader mode to attach it as a USB drive.
1. Copy `right.uf2` to the mounted drive.
1. Unplug the right side keyboard and turn it back on.
1. Enjoy!

> Note: There are also physical reset buttons on both keyboards which can be used to enter and exit the bootloader mode. Their location is described in section 2.7 on page 9 in the [User Manual](https://kinesis-ergo.com/wp-content/uploads/Advantage360-ZMK-KB360-PRO-Users-Manual-v3-10-23.pdf) and use is described in section 5.9 on page 14. 

### Upgrading from V2 to V3

If you are upgrading from V2 to V3, and if the flashing didn't work as expected (i.e. if you are unable to pair the keyboard via Bluetooth), then consider [resetting](https://kinesis-ergo.com/support/kb360pro/#firmware-updates) both halves of the keyboard to its native state. Make sure to use the `settings-reset.uf2` file from 
the V3 branch of this repository. After doing this, proceed with the flashing instructions above.

## Other support

Further support resources can be found on Kinesis.com:

* https://kinesis-ergo.com/support/kb360pro/#firmware-updates
* https://kinesis-ergo.com/support/kb360pro/#manuals
