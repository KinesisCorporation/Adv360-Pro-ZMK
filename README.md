# ADV360-PRO-ZMK

## Modifying the keymap

[The ZMK documentation](https://zmk.dev/docs) covers both basic and advanced functionality and has a table of OS compatibility for keycodes. Please note that the RGB Underglow, Backlight and Power Management sections are not relevant to the Advantage 360 Pro's custom ZMK fork. For more information see [this note](#note)

There is a GUI for editing the keymap. It is available at https://kinesiscorporation.github.io/Adv360-Pro-GUI. This repository is also compatible with certain other web based ZMK keymap editors.

Certain ZMK features require knowing the exact key positions in the matrix. They can be found in both image and text format [here](assets/key-positions.md)

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

The built docker container and compiled firmware files can be deleted with `make clean`. This might be necessary if you updated your fork from V2.0 to V3.0 and are encountering build failures

## Flashing firmware

Follow the programming instruction on page 8 of the [Quick Start Guide](https://kinesis-ergo.com/wp-content/uploads/Advantage360-Professional-QSG-v8-25-22.pdf) to flash the firmware.

### Overview

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

## Changelog

The changelog for both the config repo and the underlying ZMK fork that the config repo builds against can be found [here](CHANGELOG.md)

## Note

By default this config repository references [a customised version of ZMK](https://github.com/ReFil/zmk/tree/adv360-z3.2) with Advantage 360 Pro specific functionality and changes over [base ZMK](https://github.com/zmkfirmware/zmk). The Kinesis fork is regularly updated to bring the latest updates and changes from base ZMK however will not always be completely up to date.

Whilst the Advantage 360 Pro is compatible with base ZMK some of the more advanced features will not work, and Kinesis cannot provide customer service for usage of base ZMK. Likewise the ZMK community cannot provide support for either the Kinesis keymap editor, nor any usage of the Kinesis custom fork.

## Other support

Further support resources can be found on Kinesis.com:

* https://kinesis-ergo.com/support/kb360pro/#firmware-updates
* https://kinesis-ergo.com/support/kb360pro/#manuals
