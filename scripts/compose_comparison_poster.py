#!/usr/bin/env python3
"""Compose an original-over-generated social poster without re-rendering either panel."""

from __future__ import annotations

import argparse
import colorsys
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    from PIL import Image, ImageOps
except ImportError as exc:  # pragma: no cover - environment-specific guidance
    raise SystemExit("Pillow is required: install it with `python3 -m pip install Pillow`.") from exc


RATIOS = {"4:5": (4, 5), "9:16": (9, 16), "1:1": (1, 1)}
ALLOWED_KEYS = {
    "layout",
    "canvas_ratio",
    "canvas_width",
    "background_strategy",
    "background_color",
    "original_position",
    "generated_position",
    "fit",
    "panel_width_percent",
    "outer_margin_percent",
    "inter_panel_gap_percent",
}
HEX_COLOR = re.compile(r"^#[0-9A-Fa-f]{6}$")


def load_card(path: Path) -> dict[str, Any]:
    try:
        card = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read Social Output Card: {exc}") from exc
    if not isinstance(card, dict):
        raise ValueError("Social Output Card must be a JSON object")
    missing = ALLOWED_KEYS - set(card)
    extra = set(card) - ALLOWED_KEYS
    if missing:
        raise ValueError("missing card fields: " + ", ".join(sorted(missing)))
    if extra:
        raise ValueError("unsupported card fields: " + ", ".join(sorted(extra)))
    constants = {
        "layout": "comparison_poster",
        "original_position": "top",
        "generated_position": "bottom",
        "fit": "contain",
    }
    for key, expected in constants.items():
        if card[key] != expected:
            raise ValueError(f"{key} must be {expected!r}")
    if card["canvas_ratio"] not in RATIOS:
        raise ValueError("canvas_ratio must be 4:5, 9:16, or 1:1")
    width = card["canvas_width"]
    if not isinstance(width, int) or isinstance(width, bool) or not 720 <= width <= 2160:
        raise ValueError("canvas_width must be an integer from 720 to 2160")
    for key, low, high in (
        ("panel_width_percent", 60, 92),
        ("outer_margin_percent", 4, 15),
        ("inter_panel_gap_percent", 2, 10),
    ):
        value = card[key]
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not low <= value <= high:
            raise ValueError(f"{key} must be between {low} and {high}")
    strategy = card["background_strategy"]
    color = card["background_color"]
    if strategy == "source_warm":
        if color is not None:
            raise ValueError("background_color must be null for source_warm")
    elif strategy == "custom":
        if not isinstance(color, str) or not HEX_COLOR.fullmatch(color):
            raise ValueError("custom background_color must use #RRGGBB")
    else:
        raise ValueError("background_strategy must be source_warm or custom")
    return card


def source_warm_background(image: Image.Image) -> tuple[int, int, int]:
    sample = image.convert("RGB")
    sample.thumbnail((72, 72), Image.Resampling.LANCZOS)
    candidates: list[tuple[float, tuple[int, int, int]]] = []
    all_pixels = list(sample.getdata())
    for rgb in all_pixels:
        r, g, b = (channel / 255 for channel in rgb)
        hue, saturation, value = colorsys.rgb_to_hsv(r, g, b)
        degrees = hue * 360
        warm = degrees <= 78 or degrees >= 330
        if warm and 0.07 <= saturation <= 0.85 and 0.25 <= value <= 0.97:
            light_preference = 1 - abs(value - 0.68)
            score = (0.35 + saturation) * max(light_preference, 0.15)
            candidates.append((score, rgb))
    if candidates:
        candidates.sort(reverse=True, key=lambda item: item[0])
        selected = [rgb for _, rgb in candidates[: max(12, len(candidates) // 3)]]
    else:
        selected = all_pixels or [(196, 171, 142)]
    seed = tuple(round(sum(pixel[index] for pixel in selected) / len(selected)) for index in range(3))
    paper = (247, 232, 211)
    mixed = tuple(round(seed[index] * 0.24 + paper[index] * 0.76) for index in range(3))
    hue, lightness, saturation = colorsys.rgb_to_hls(*(channel / 255 for channel in mixed))
    lightness = min(0.93, max(0.82, lightness))
    saturation = min(0.34, max(0.12, saturation))
    return tuple(round(channel * 255) for channel in colorsys.hls_to_rgb(hue, lightness, saturation))


def parse_hex_color(value: str) -> tuple[int, int, int]:
    return tuple(int(value[index : index + 2], 16) for index in (1, 3, 5))


def contain(image: Image.Image, width: int, height: int) -> Image.Image:
    result = image.copy()
    result.thumbnail((max(1, width), max(1, height)), Image.Resampling.LANCZOS)
    return result


def compose(original_path: Path, generated_path: Path, output_path: Path, card: dict[str, Any]) -> tuple[int, int, tuple[int, int, int]]:
    with Image.open(original_path) as raw_original, Image.open(generated_path) as raw_generated:
        original = ImageOps.exif_transpose(raw_original).convert("RGB")
        generated = ImageOps.exif_transpose(raw_generated).convert("RGB")

    ratio_width, ratio_height = RATIOS[card["canvas_ratio"]]
    canvas_width = card["canvas_width"]
    canvas_height = round(canvas_width * ratio_height / ratio_width)
    margin = round(min(canvas_width, canvas_height) * card["outer_margin_percent"] / 100)
    gap = round(min(canvas_width, canvas_height) * card["inter_panel_gap_percent"] / 100)
    panel_width = round(canvas_width * card["panel_width_percent"] / 100)
    slot_height = (canvas_height - 2 * margin - gap) // 2
    if slot_height <= 0 or panel_width <= 0:
        raise ValueError("layout percentages leave no room for the image panels")

    if card["background_strategy"] == "source_warm":
        background = source_warm_background(original)
    else:
        background = parse_hex_color(card["background_color"])
    canvas = Image.new("RGB", (canvas_width, canvas_height), background)

    top = contain(original, panel_width, slot_height)
    bottom = contain(generated, panel_width, slot_height)
    top_x = (canvas_width - top.width) // 2
    top_y = margin + (slot_height - top.height) // 2
    bottom_slot_y = margin + slot_height + gap
    bottom_x = (canvas_width - bottom.width) // 2
    bottom_y = bottom_slot_y + (slot_height - bottom.height) // 2
    canvas.paste(top, (top_x, top_y))
    canvas.paste(bottom, (bottom_x, bottom_y))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    suffix = output_path.suffix.lower()
    if suffix in {".jpg", ".jpeg"}:
        canvas.save(output_path, quality=94, subsampling=0)
    else:
        canvas.save(output_path, format="PNG", optimize=True)
    return canvas_width, canvas_height, background


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--original", type=Path, required=True)
    parser.add_argument("--generated", type=Path, required=True)
    parser.add_argument("--card", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        card = load_card(args.card)
        width, height, background = compose(args.original, args.generated, args.output, card)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(
        f"CREATED: {args.output} ({width}x{height}, background "
        f"#{background[0]:02X}{background[1]:02X}{background[2]:02X})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
