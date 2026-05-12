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
import re
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined

TOTAL_KEYS = 76
ROW_SIZES = [14, 14, 18, 14, 16]  # Must sum to 76 (used for output formatting)
TEMPLATE_FILE = "adv360.keymap.j2"
PROFILE_SOURCE_FILE = "adv360.keymap.original"

# Physical key-position layout from assets/key-positions.md.
LAYOUT_GROUPS = [
    [[0, 1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12, 13]],
    [[14, 15, 16, 17, 18, 19, 20], [21, 22, 23, 24, 25, 26, 27]],
    [[28, 29, 30, 31, 32, 33, 34], [35, 36, 37, 38], [39, 40, 41, 42, 43, 44, 45]],
    [[46, 47, 48, 49, 50, 51], [52, 53], [54, 55, 56, 57, 58, 59]],
    [[60, 61, 62, 63, 64], [65, 66, 67], [68, 69, 70], [71, 72, 73, 74, 75]],
]

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


def _extract_row_starts_from_layer(text: str, layer_name: str, row_sizes: list[int]) -> list[list[int]] | None:
    """Extract per-row binding start columns for a single layer block."""
    layer_match = re.search(
        rf"\n\s*{layer_name}\s*\{{.*?bindings\s*=\s*<\n(.*?)\n\s*>;",
        text,
        re.S,
    )
    if not layer_match:
        return None

    binding_lines = layer_match.group(1).splitlines()
    if len(binding_lines) != len(row_sizes):
        return None

    row_starts: list[list[int]] = []
    for row_idx, line in enumerate(binding_lines):
        starts = [idx for idx, ch in enumerate(line) if ch == "&"]
        expected = row_sizes[row_idx]
        if len(starts) != expected:
            return None

        base = starts[0]
        row_starts.append([s - base for s in starts])

    return row_starts


def extract_original_layer_profiles(profile_path: Path, row_sizes: list[int]) -> dict[str, list[list[int]]]:
    """Extract per-layer row start profiles from adv360.keymap.original."""
    if not profile_path.exists():
        return {}

    text = profile_path.read_text()
    profiles: dict[str, list[list[int]]] = {}
    for layer_name in ("default_layer", "keypad", "fn", "mod"):
        starts = _extract_row_starts_from_layer(text, layer_name, row_sizes)
        if starts:
            profiles[layer_name] = starts
    return profiles


def format_row_with_starts(tokens: list[str], starts: list[int]) -> str:
    """Place bindings at fixed start columns, preserving original visual layout."""
    if not tokens:
        return ""

    out = []
    cursor = 0
    for idx, token in enumerate(tokens):
        target = starts[idx] if idx < len(starts) else cursor + 1
        if idx == 0:
            target = 0
        if target < cursor:
            target = cursor + 1
        out.append(" " * (target - cursor))
        out.append(token)
        cursor = target + len(token)

    return "".join(out).rstrip()


def format_bindings_lines(bindings: list[str], row_starts: list[list[int]]) -> list[str]:
    """Format bindings by explicit physical key position groups and profile starts."""
    lines = []
    for row_idx, groups in enumerate(LAYOUT_GROUPS):
        row_positions = []
        for group in groups:
            row_positions.extend(group)

        row_tokens = [bindings[pos] for pos in row_positions]

        if row_idx >= len(row_starts):
            raise ValueError(f"Missing profile row starts for row {row_idx}")
        if len(row_starts[row_idx]) != len(row_tokens):
            raise ValueError(
                f"Profile row {row_idx} has {len(row_starts[row_idx])} starts; expected {len(row_tokens)}"
            )

        lines.append(format_row_with_starts(row_tokens, row_starts[row_idx]))
    return lines


def build_behavior_entries(behaviors: dict) -> list[dict]:
    """Convert behavior config into template-ready entries."""
    entries = []
    for behavior_id, config in behaviors.items():
        entries.append(
            {
                "id": behavior_id,
                "name": config.get("name", behavior_id),
                "compatible": config["compatible"],
                "label": config["label"],
                "binding_cells": config["binding_cells"],
                "tapping_term_ms": config["tapping_term_ms"],
                "quick_tap_ms": config["quick_tap_ms"],
                "flavor": config["flavor"],
                "bindings": [f"<{binding}>" for binding in config["bindings"]],
            }
        )
    return entries


def normalize_layer(layer: dict, row_sizes: list[int]) -> dict:
    """Normalize and validate layer for template rendering."""
    name = layer["name"]
    display_name = layer.get("display_name", name)

    if layer.get("status") == "reserved":
        return {
            "name": name,
            "display_name": display_name,
            "status": "reserved",
        }

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

    return {
        "name": name,
        "display_name": display_name,
        "status": "active",
        "bindings": converted,
    }


def generate_keymap(config: dict, template_dir: Path, profile_path: Path) -> str:
    """Generate the complete keymap file content from a Jinja template."""
    behaviors = config.get("behaviors", {})
    raw_layers = config.get("layers", [])

    layers = [normalize_layer(layer, ROW_SIZES) for layer in raw_layers]
    layer_profiles = extract_original_layer_profiles(profile_path, ROW_SIZES)
    if "default_layer" not in layer_profiles:
        raise ValueError(f"Required profile layer 'default_layer' not found in {profile_path}")
    default_profile = layer_profiles.get("default_layer")
    for layer in layers:
        if layer["status"] != "reserved":
            row_starts = layer_profiles.get(layer["name"], default_profile)
            if row_starts is None:
                raise ValueError(f"No spacing profile available for layer '{layer['name']}'")
            layer["binding_lines"] = format_bindings_lines(layer["bindings"], row_starts)

    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        undefined=StrictUndefined,
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template(TEMPLATE_FILE)
    return template.render(
        behaviors=build_behavior_entries(behaviors),
        layers=layers,
    ) + "\n"


def main():
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parents[1]

    parser = argparse.ArgumentParser(description="Generate ZMK keymap from YAML")
    parser.add_argument("--check", action="store_true", help="Validate only")
    parser.add_argument(
        "--output",
        "-o",
        default=str((repo_root / "config" / "adv360.keymap").resolve()),
        help="Output file",
    )
    parser.add_argument(
        "--input",
        "-i",
        default=str((script_dir / "keymap.yaml").resolve()),
        help="Input YAML file",
    )
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()
    profile_path = repo_root / "config" / PROFILE_SOURCE_FILE

    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    with open(input_path) as f:
        config = yaml.safe_load(f)

    try:
        output = generate_keymap(config, script_dir, profile_path)
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
