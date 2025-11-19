# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a ZMK (Zephyr Mechanical Keyboard) firmware repository for the Kinesis Advantage 360 Pro split ergonomic keyboard. The firmware is built using the Zephyr RTOS and produces `.uf2` files that are flashed to the left and right keyboard halves.

## Build Commands

### Local Development (Container-based)
- **Build both halves**: `make` - Builds left and right firmware using Docker/Podman
- **Build left only**: `make left` - Only builds firmware for the left half (faster for testing)
- **Clean firmware only**: `make clean_firmware` - Removes compiled `.uf2` files but keeps container
- **Clean container only**: `make clean_image` - Removes Docker container but keeps firmware files
- **Full clean**: `make clean` - Removes both compiled firmware and Docker images
- **Built firmware location**: `firmware/` directory (format: `YYYYMMDDHHMM-COMMIT-left.uf2` and `YYYYMMDDHHMM-COMMIT-right.uf2`)

### CI/CD
- GitHub Actions automatically builds firmware on push, pull request, or manual dispatch
- Artifacts are uploaded as timestamped files with commit hash in filename

### Manual West Commands (inside container)
```bash
west build -s zmk/app -d build/left -b adv360_left -- -DZMK_CONFIG="${PWD}/config"
west build -s zmk/app -d build/right -b adv360_right -- -DZMK_CONFIG="${PWD}/config"
```

## Architecture

### Split Keyboard Structure
The Advantage 360 Pro is a split keyboard requiring separate firmware for left and right halves:
- **Left half**: Built with target `adv360_left`
- **Right half**: Built with target `adv360_right`
- Both halves communicate wirelessly and each connects to the host independently

### Key Configuration Files

#### Keymap Files
- `config/adv360.keymap` - Main keymap definition with 4 layers (generated file, may be auto-generated)
- `config/keymap.json` - JSON representation of the keymap with layer names: base, keypad, fn, mod
- `config/macros.dtsi` - Custom macro definitions included in the main keymap
- Layer structure:
  - Layer 0 (base): Default QWERTY layout
  - Layer 1 (keypad): Numeric keypad layer
  - Layer 2 (fn): Function keys and media controls
  - Layer 3 (mod): Bluetooth, RGB, backlight controls, and bootloader access

#### Board Definitions
- `config/boards/arm/adv360/*.dts` - Device tree files for hardware configuration
- `config/boards/arm/adv360/adv360.dtsi` - Shared device tree includes (nRF52840 based)
- `config/boards/arm/adv360/*_defconfig` - Board-specific Kconfig defaults

#### Build Configuration
- `config/west.yml` - West manifest pointing to ZMK fork (refil/zmk @ adv360-z3.5-2 branch)
- `config/info.json` - Keyboard layout metadata with 88-key physical layout definition
- `config/version.dtsi` - Auto-generated version info (timestamp, branch, commit), accessed via Mod+V macro

### ZMK/Zephyr Integration
- Uses West workspace management tool
- ZMK source is pulled from a fork: `https://github.com/refil/zmk` (branch: adv360-z3.5-2)
- Base image: `zmkfirmware/zmk-build-arm:stable`
- The build process runs `west init`, `west update`, and `west zephyr-export` to set up the environment

### Container Build Flow
1. `bin/get_version_local.sh` generates version metadata in `config/version.dtsi`
2. Dockerfile pulls ZMK dependencies and initializes West workspace
3. `bin/build.sh` builds left half (and optionally right half based on `BUILD_RIGHT` env var)
4. Outputs are copied to `firmware/` with timestamp and commit hash
5. Makefile resets `config/version.dtsi` after build to prevent unnecessary git diffs
6. Makefile handles Docker/Podman detection and volume mounting with SELinux compatibility

## Important Notes

### Keymap Modifications
- **Recommended**: Use Nick Coutsos's keymap editor (https://nickcoutsos.github.io/keymap-editor/) for GitHub-based editing
- **Alternative**: One-time upgrade to Clique for web-based configuration (https://kinesis-ergo.com/360p-clique-upgrade/)
- When editing keymaps manually, modify both `config/adv360.keymap` (devicetree format) and `config/keymap.json` (JSON format)
- The keymap comment states "THIS FILE WAS GENERATED" - prefer using the keymap editor tools
- Keymap uses ZMK behavior bindings: `&kp` (key press), `&mo` (momentary layer), `&tog` (toggle layer), `&bt` (bluetooth), `&rgb_ug` (RGB underglow), `&bl` (backlight)
- Key positions for advanced features (combos, etc.) documented in `assets/key-positions.md` and `assets/key-positions.png`

### Hardware-Specific Features
- **Bluetooth pairing**: Managed through layer 3 (mod layer) with `&bt BT_SEL N` and `&bt BT_CLR`
- **Battery reporting**: Disabled by default (can cause spontaneous wake); enable via `CONFIG_BT_BAS=y` in `adv360_left_defconfig`
- **N-Key Rollover**: Enabled by default; extended range (F13-F24, INTL1-9) can be enabled via `CONFIG_ZMK_HID_KEYBOARD_EXTENDED_REPORT=y`
- **Layer indicator LEDs**: Each layer (0-31 supported) displays specific colors on left/right modules
- **Modifier indicator color**: Configurable via `CONFIG_ZMK_RGB_UNDERGLOW_MOD_COLOR=0xRRGGBB` in defconfig files
- **RGB underglow and backlight controls**: Available on mod layer
- **Pedal inputs**: Supported (Ped1-4 positions defined in info.json)
- **Bootloader access**: Via Mod+macro1 (left) and Mod+macro3 (right), or physical reset buttons

### Flashing Firmware
1. Extract firmware files from GitHub artifacts or `firmware/` folder
2. Left side: Connect USB, press Mod+macro1 for bootloader, copy `left.uf2`
3. Right side: Connect USB, press Mod+macro3 for bootloader, copy `right.uf2`
4. Physical reset buttons also available (see User Manual section 2.7)
5. Settings reset files available for firmware upgrades (see Kinesis support site)

### Versioning
- Firmware version accessible via Mod+V macro (format: YYYYMMDD-XXXX-YYYYYY)
- GitHub Actions builds include timestamp and commit hash in filename
- `config/version.dtsi` auto-generated during build, don't commit changes

### Git Workflow
- Main branch: `V3.0` (current), previous was `V2.0`
- Upgrading from V2.0 to V3.0 requires special process (see `UPGRADE.md` and Kinesis support docs)
- When committing keymap changes, commit `config/adv360.keymap` and related files
- Firmware binaries in `firmware/` directory are gitignored
- `config/version.dtsi` is reset after builds to prevent spurious diffs

### Troubleshooting
- If build fails after updating from V2.0 to V3.0, run `make clean` to remove stale containers
- macOS users with Apple Silicon: Start colima with `colima start --arch x86_64`
- For merge conflicts during V2→V3 upgrade, see `UPGRADE.md`
