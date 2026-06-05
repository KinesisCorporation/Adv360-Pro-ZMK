# Adv360-Pro-ZMK

ZMK firmware configuration for the Kinesis Advantage 360 Pro keyboard.

## Project structure

- `config/adv360.keymap` - Main keymap definition (layers, bindings, behaviors)
- `config/macros.dtsi` / `config/version.dtsi` - Macros and version info included by the keymap
- `config/west.yml` - ZMK west manifest (points to the Kinesis ZMK fork)
- `Makefile` - Local build via Docker/Podman container
- `firmware/` - Build output (`.uf2` files)

## Building

- `make` - Build firmware for both halves
- `make left` - Build left half only
- `make clean` - Remove built firmware and Docker image

Requires Docker or Podman. On macOS with Apple Silicon, use `colima start --arch x86_64`.

## Commits

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>: <description>

[optional body]
```

Types: `feat`, `fix`, `docs`, `chore`, `refactor`, `build`, `ci`
