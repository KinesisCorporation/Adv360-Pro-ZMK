#!/usr/bin/env python3
"""
Generate adv360.keymap from keymap.yaml

Usage:
    python generate_keymap.py [--check] [--output FILE]

Options:
    --check     Validate only, don't write output
    --output    Output file path (default: adv360.keymap)
"""

import argparse
import sys
from pathlib import Path

import yaml

TOTAL_KEYS = 76
ROW_SIZES = [14, 14, 18, 14, 16]  # Must sum to 76 (used for output formatting)

LAYER_BEHAVIORS = {
    "mo", "tog", "lt", "to", "sl",
}

SPECIAL_BEHAVIORS = {
    "bt", "rgb_ug", "bl", "stp", "mkp", "ext_power",
}

PASSTHROUGH_BEHAVIORS = {
    "none", "trans",
}

MACROS = {
    "macro_quotes", "macro_dquotes", "macro_braces", "macro_parens",
    "macro_brackets", "macro_kinesis", "macro_ver",
    "Win_Cut", "Win_Copy", "Win_Paste", "Win_Select_All", "Win_Undo",
    "Win_Desktop", "Win_File_Explorer", "Win_Snip_Tool", "Win_Show_All_Windows",
    "Win_Close_Program", "Win_Settings_Menu", "Win_Lock_PC",
    "Win_Tile_Left", "Win_Tile_Up", "Win_Tile_Down", "Win_Tile_Right",
    "Mac_Cut", "Mac_Copy", "Mac_Paste", "Mac_Undo", "Mac_Select_All",
    "Mac_Mission_Control", "Mac_Snip_Tool", "Mac_Spotlight_Search",
    "Mac_Close_Program", "Mac_Strike_Through_Text", "Double_Click",
}

RAW_BEHAVIORS = {
    "bootloader", "studio_unlock", "sys_reset", "soft_off",
}


def convert_key(key: str) -> str:
    """Convert a YAML key definition to ZMK binding syntax."""
    key = str(key).strip()

    if key.startswith("&"):
        return key

    if key in PASSTHROUGH_BEHAVIORS:
        return f"&{key}"

    parts = key.split()
    first = parts[0]

    if first in RAW_BEHAVIORS:
        return f"&{key}"

    if first in MACROS:
        return f"&{key}"

    if first in LAYER_BEHAVIORS:
        return f"&{key}"

    if first in SPECIAL_BEHAVIORS:
        return f"&{key}"

    if first == "hm":
        return f"&{key}"

    return f"&kp {key}"


def expand_shorthand(bindings, total_keys: int = TOTAL_KEYS) -> list[str]:
    """Expand shorthand bindings like 'none' or 'trans' to full key list."""
    if isinstance(bindings, str):
        if bindings in ("none", "trans"):
            return [f"&{bindings}"] * total_keys
        raise ValueError(f"Unknown shorthand binding: {bindings}")
    return None


def bindings_from_dict(bindings: dict, total_keys: int = TOTAL_KEYS) -> list[str]:
    """Convert key-position dictionary to ordered list of bindings."""
    result = ["&none"] * total_keys  # Default unspecified keys to &none
    
    for key, value in bindings.items():
        # Skip comments (YAML keys that aren't integers)
        try:
            pos = int(key)
        except (ValueError, TypeError):
            continue
        
        if pos < 0 or pos >= total_keys:
            raise ValueError(f"Key position {pos} out of range (0-{total_keys - 1})")
        
        result[pos] = convert_key(value)
    
    return result


def flatten_bindings(rows: list[list[str]]) -> list[str]:
    """Flatten row-based bindings into a single list (legacy support)."""
    flat = []
    for row in rows:
        flat.extend(row)
    return flat


def validate_layer(name: str, bindings: list[str], row_sizes: list[int]) -> list[str]:
    """Validate layer has correct key count and return errors."""
    errors = []
    expected = sum(row_sizes)
    actual = len(bindings)

    if actual != expected:
        errors.append(f"Layer '{name}': expected {expected} keys, got {actual}")

    return errors


def format_bindings_block(bindings: list[str], row_sizes: list[int]) -> str:
    """Format bindings into the keymap file format with proper spacing."""
    lines = []
    idx = 0

    for row_idx, size in enumerate(row_sizes):
        row_bindings = bindings[idx:idx + size]
        idx += size

        formatted = " ".join(row_bindings)
        lines.append(f"        {formatted}")

    return "\n".join(lines)


def generate_behavior_block(behaviors: dict) -> str:
    """Generate the behaviors block from YAML config."""
    if not behaviors:
        return ""

    lines = []
    for name, config in behaviors.items():
        label_name = config.get("name", name)
        lines.append(f"      {name}: {label_name} {{")
        lines.append(f'          compatible = "{config["compatible"]}";')
        lines.append(f'          label = "{config["label"]}";')
        lines.append(f'          #binding-cells = <{config["binding_cells"]}>;')
        lines.append(f'          tapping-term-ms = <{config["tapping_term_ms"]}>;')
        lines.append(f'          quick_tap_ms = <{config["quick_tap_ms"]}>;')
        lines.append(f'          flavor = "{config["flavor"]}";')

        bindings_str = ", ".join(f"<{b}>" for b in config["bindings"])
        lines.append(f"          bindings = {bindings_str};")
        lines.append("      };")

    return "\n".join(lines)


def generate_layer_block(layer: dict, row_sizes: list[int]) -> str:
    """Generate a single layer block."""
    name = layer["name"]
    display_name = layer.get("display_name", name)

    if layer.get("status") == "reserved":
        return f'''    {name} {{ 
      display-name = "{display_name}";    
      status = "reserved";
    }};'''

    bindings = layer.get("bindings")
    if bindings is None:
        raise ValueError(f"Layer '{name}' has no bindings defined")

    expanded = expand_shorthand(bindings)
    if expanded:
        converted = expanded
    elif isinstance(bindings, dict):
        converted = bindings_from_dict(bindings)
    elif isinstance(bindings, list):
        # Legacy row-based format
        flat = flatten_bindings(bindings)
        converted = [convert_key(k) for k in flat]
    else:
        raise ValueError(f"Layer '{name}': invalid bindings format")

    errors = validate_layer(name, converted, row_sizes)
    if errors:
        raise ValueError("\n".join(errors))

    bindings_block = format_bindings_block(converted, row_sizes)

    return f'''    {name} {{
      display-name = "{display_name}";
      bindings = <
{bindings_block}
      >;
    }};'''


def generate_keymap(config: dict) -> str:
    """Generate the complete keymap file content."""
    behaviors = config.get("behaviors", {})
    layers = config.get("layers", [])

    behavior_block = generate_behavior_block(behaviors)

    layer_blocks = []
    for layer in layers:
        layer_blocks.append(generate_layer_block(layer, ROW_SIZES))

    layers_content = "\n".join(layer_blocks)

    return f'''#include <behaviors.dtsi>
#include <dt-bindings/zmk/keys.h>
#include <dt-bindings/zmk/bt.h>
#include <dt-bindings/zmk/rgb.h>
#include <dt-bindings/zmk/stp.h>
#include <dt-bindings/zmk/backlight.h>
#include <dt-bindings/zmk/pointing.h>

/ {{
    behaviors {{
      #include "macros.dtsi"
      #include "version.dtsi"

{behavior_block}
    }};

  keymap {{
    compatible = "zmk,keymap";

{layers_content}
  }};
}};
'''


def main():
    parser = argparse.ArgumentParser(description="Generate ZMK keymap from YAML")
    parser.add_argument("--check", action="store_true", help="Validate only")
    parser.add_argument("--output", "-o", default="adv360.keymap", help="Output file")
    parser.add_argument("--input", "-i", default="keymap.yaml", help="Input YAML file")
    args = parser.parse_args()

    script_dir = Path(__file__).parent
    input_path = script_dir / args.input
    output_path = script_dir / args.output

    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    with open(input_path) as f:
        config = yaml.safe_load(f)

    try:
        output = generate_keymap(config)
    except ValueError as e:
        print(f"Validation error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.check:
        print(f"Validation passed: {input_path}")
        sys.exit(0)

    with open(output_path, "w") as f:
        f.write(output)

    print(f"Generated: {output_path}")


if __name__ == "__main__":
    main()
