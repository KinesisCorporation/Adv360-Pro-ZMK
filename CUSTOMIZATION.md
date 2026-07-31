# macOS Home-Row Mods and Nav Layer

This configuration is based on the official Kinesis `V3.0` keymap. It preserves
the stock Base, Keypad, Fn, and Mod layers.

## Base-layer changes

### Home-row modifiers

| Key | Tap | Hold |
| --- | --- | --- |
| A | A | Left Command |
| S | S | Left Option |
| D | D | Left Control |
| F | F | Left Shift |
| J | J | Right Shift |
| K | K | Right Control |
| L | L | Right Option |
| ; | ; | Right Command |

The home-row modifiers use opposite-hand positional hold-tap. A key typed on
the same half resolves as its normal letter, minimizing modifier errors during
ordinary rolls. The initial timing is 280 ms tap/hold, 175 ms quick-tap, and
150 ms prior-idle.

### Thumb clusters

Left: Space, Forward Delete, Control, Option, Home, End.

Right: Backspace, Enter, Command, Control, Page Up, Page Down.

This swaps the stock Space and Backspace locations; the other thumb actions
remain in their stock physical locations.

### Nav layer

Tap Caps Lock for Caps Lock. Hold it to momentarily enter Nav (layer 4):

| Hold Caps, press | Output |
| --- | --- |
| H | Left Arrow |
| J | Down Arrow |
| K | Up Arrow |
| L | Right Arrow |

Every other Nav-layer key is transparent.

## Build and flash

The repository builds a separate `.uf2` firmware file for the left and right
modules. Do not flash either half until the build succeeds and both files are
available. Flash the matching left file to the left module and the matching
right file to the right module.

The official workflow is to fork this repository, push this change to the fork,
download the GitHub Actions firmware artifact, then flash the two files.
