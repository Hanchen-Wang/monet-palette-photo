#!/usr/bin/env python3
"""Validate a Monet Transformation Card using only the Python standard library."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


MODES = {
    "full_impression": "none_retained",
    "subject_monetization": "none_retained",
    "atmospheric_monetization": "partial_required",
    "zine_hybrid": "partial_required",
    "distilled_monet": "none_retained",
}
STRENGTHS = {"M1", "M2", "M3", "M4"}
PRESENTATION_PROFILES = {"immersive", "sparse_social"}
ZINE_STRATEGIES = {"not_applicable", "integrated_field", "cutout_isolation"}
GRAPHIC_GRAMMARS = {"silhouette", "contour", "field", "rhythm", "cutout"}
ORIENTATIONS = {"portrait", "landscape", "square"}
BRUSH_FAMILIES = {
    "broken_dabs",
    "short_directional",
    "horizontal_shimmer",
    "vertical_veil",
    "broad_flat_patches",
    "feathered_atmosphere",
}
EDGE_LEVELS = {"L1", "L2", "L3", "L4"}
BACKGROUNDS = {"preserve", "simplify", "line", "paper"}
TRANSITIONS = {"brush_intrusion", "dissolve", "light_bridge", "reflection_bridge", "torn_field", "none"}
SCORE_FIELDS = ("light", "atmosphere", "reflection", "color_variation", "edge_instability")
REQUIRED_TOP = {
    "mode",
    "strength",
    "presentation_profile",
    "shape_abstraction",
    "zine_strategy",
    "zine_cutout_plan",
    "source_pixel_policy",
    "source_orientation",
    "semantic_anchor",
    "primary_subject",
    "supporting_elements",
    "spatial_invariants",
    "protected_elements",
    "discard",
    "impressionability_candidates",
    "primary_monet_zone",
    "primary_zone_override",
    "secondary_monet_zones",
    "preserve_photo_zones",
    "simplify_zones",
    "line_zones",
    "negative_space_zones",
    "light_card",
    "palette_families",
    "brush_map",
    "edge_map",
    "background_treatment",
    "transition_strategy",
    "composition",
    "visible_text",
}


def nonempty_string(value: Any, path: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{path} must be a non-empty string")


def string_array(
    value: Any,
    path: str,
    errors: list[str],
    *,
    min_items: int = 0,
    max_items: int | None = None,
) -> list[str]:
    if not isinstance(value, list):
        errors.append(f"{path} must be an array")
        return []
    if len(value) < min_items:
        errors.append(f"{path} must contain at least {min_items} item(s)")
    if max_items is not None and len(value) > max_items:
        errors.append(f"{path} must contain at most {max_items} item(s)")
    if any(not isinstance(item, str) or not item.strip() for item in value):
        errors.append(f"{path} must contain only non-empty strings")
        return []
    if len(set(value)) != len(value):
        errors.append(f"{path} contains duplicate values")
    return value


def validate(data: Any) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(data, dict):
        return ["card root must be a JSON object"], warnings

    missing = sorted(REQUIRED_TOP - set(data))
    extra = sorted(set(data) - REQUIRED_TOP)
    if missing:
        errors.append("missing required fields: " + ", ".join(missing))
    if extra:
        errors.append("unsupported fields: " + ", ".join(extra))
    if missing:
        return errors, warnings

    mode = data["mode"]
    if mode not in MODES:
        errors.append(f"mode must be one of: {', '.join(sorted(MODES))}")
    elif data["source_pixel_policy"] != MODES[mode]:
        errors.append(f"{mode} requires source_pixel_policy={MODES[mode]}")
    if data["strength"] not in STRENGTHS:
        errors.append("strength must be M1, M2, M3, or M4")
    profile = data["presentation_profile"]
    if profile not in PRESENTATION_PROFILES:
        errors.append("presentation_profile must be immersive or sparse_social")
    zine_strategy = data["zine_strategy"]
    zine_plan = data["zine_cutout_plan"]
    if zine_strategy not in ZINE_STRATEGIES:
        errors.append("zine_strategy must be not_applicable, integrated_field, or cutout_isolation")
    if mode == "zine_hybrid":
        if zine_strategy not in {"integrated_field", "cutout_isolation"}:
            errors.append("zine_hybrid requires zine_strategy=integrated_field or cutout_isolation")
    elif zine_strategy != "not_applicable":
        errors.append("non-Zine modes require zine_strategy=not_applicable")
    if zine_strategy != "cutout_isolation" and zine_plan is not None:
        errors.append("zine_cutout_plan must be null unless zine_strategy=cutout_isolation")
    if zine_strategy == "cutout_isolation" and profile != "sparse_social":
        errors.append("cutout_isolation requires presentation_profile=sparse_social")
    if data["source_orientation"] not in ORIENTATIONS:
        errors.append("source_orientation must be portrait, landscape, or square")

    shape = data["shape_abstraction"]
    if profile == "immersive":
        if shape is not None:
            errors.append("immersive cards require shape_abstraction=null")
    elif profile == "sparse_social":
        expected_shape = {
            "semantic_minimum",
            "dominant_gesture",
            "source_shape_candidates",
            "retain",
            "merge",
            "omit",
            "transform",
            "expose",
            "primary_grammar",
            "supporting_grammar",
            "detail_removal_percent",
            "quiet_area_percent",
            "active_shape_percent",
            "thumbnail_anchor",
        }
        if not isinstance(shape, dict) or set(shape) != expected_shape:
            errors.append("shape_abstraction has missing or unsupported fields")
        else:
            for field in ("semantic_minimum", "dominant_gesture", "thumbnail_anchor"):
                nonempty_string(shape[field], f"shape_abstraction.{field}", errors)
            string_array(
                shape["source_shape_candidates"],
                "shape_abstraction.source_shape_candidates",
                errors,
                min_items=1,
                max_items=2,
            )
            retained = string_array(
                shape["retain"], "shape_abstraction.retain", errors, min_items=1, max_items=2
            )
            string_array(shape["merge"], "shape_abstraction.merge", errors)
            omitted = string_array(shape["omit"], "shape_abstraction.omit", errors, min_items=1)
            string_array(shape["transform"], "shape_abstraction.transform", errors, min_items=1)
            string_array(shape["expose"], "shape_abstraction.expose", errors, min_items=1)
            if set(retained).intersection(omitted):
                errors.append("shape_abstraction.retain and omit cannot overlap")
            primary_grammar = shape["primary_grammar"]
            supporting_grammar = shape["supporting_grammar"]
            if primary_grammar not in GRAPHIC_GRAMMARS:
                errors.append("shape_abstraction.primary_grammar is invalid")
            if supporting_grammar is not None and supporting_grammar not in GRAPHIC_GRAMMARS:
                errors.append("shape_abstraction.supporting_grammar is invalid")
            if supporting_grammar == primary_grammar:
                errors.append("supporting_grammar must differ from primary_grammar")
            budgets = {
                "detail_removal_percent": (60, 90),
                "quiet_area_percent": (30, 60) if zine_strategy == "cutout_isolation" else (45, 85),
                "active_shape_percent": (35, 65) if zine_strategy == "cutout_isolation" else (10, 35),
            }
            for field, (low, high) in budgets.items():
                value = shape[field]
                if not isinstance(value, int) or isinstance(value, bool) or not low <= value <= high:
                    errors.append(f"shape_abstraction.{field} must be an integer from {low} to {high}")
            quiet = shape["quiet_area_percent"]
            active = shape["active_shape_percent"]
            if isinstance(quiet, int) and isinstance(active, int) and quiet + active > 100:
                errors.append("quiet_area_percent plus active_shape_percent cannot exceed 100")

    nonempty_string(data["semantic_anchor"], "semantic_anchor", errors)
    nonempty_string(data["primary_subject"], "primary_subject", errors)
    supporting = string_array(data["supporting_elements"], "supporting_elements", errors, min_items=1, max_items=3)
    string_array(data["spatial_invariants"], "spatial_invariants", errors, min_items=1)
    protected = string_array(data["protected_elements"], "protected_elements", errors)
    string_array(data["discard"], "discard", errors, min_items=1)
    if not supporting:
        warnings.append("the source has no validated supporting context")

    candidates = data["impressionability_candidates"]
    candidate_totals: dict[str, int] = {}
    if not isinstance(candidates, list) or not candidates:
        errors.append("impressionability_candidates must be a non-empty array")
    else:
        for index, candidate in enumerate(candidates):
            path = f"impressionability_candidates[{index}]"
            if not isinstance(candidate, dict):
                errors.append(f"{path} must be an object")
                continue
            expected = {"zone", *SCORE_FIELDS, "total", "rationale"}
            if set(candidate) != expected:
                errors.append(f"{path} has missing or unsupported fields")
                continue
            nonempty_string(candidate["zone"], f"{path}.zone", errors)
            nonempty_string(candidate["rationale"], f"{path}.rationale", errors)
            scores: list[int] = []
            for field in SCORE_FIELDS:
                value = candidate[field]
                if not isinstance(value, int) or not 0 <= value <= 4:
                    errors.append(f"{path}.{field} must be an integer from 0 to 4")
                else:
                    scores.append(value)
            if isinstance(candidate["total"], int) and len(scores) == len(SCORE_FIELDS):
                if candidate["total"] != sum(scores):
                    errors.append(f"{path}.total must equal the five score fields")
            else:
                errors.append(f"{path}.total must be an integer")
            zone = candidate.get("zone")
            if isinstance(zone, str) and zone:
                if zone in candidate_totals:
                    errors.append(f"duplicate impressionability zone: {zone}")
                elif isinstance(candidate.get("total"), int):
                    candidate_totals[zone] = candidate["total"]

    primary = data["primary_monet_zone"]
    nonempty_string(primary, "primary_monet_zone", errors)
    secondary = string_array(data["secondary_monet_zones"], "secondary_monet_zones", errors, max_items=2)
    preserve = string_array(data["preserve_photo_zones"], "preserve_photo_zones", errors)
    simplify_zones = string_array(data["simplify_zones"], "simplify_zones", errors)
    line_zones = string_array(data["line_zones"], "line_zones", errors)
    negative_zones = string_array(data["negative_space_zones"], "negative_space_zones", errors)
    if profile == "sparse_social" and not negative_zones:
        errors.append("sparse_social requires at least one negative_space_zone")

    monet_zones = {primary, *secondary}
    if primary not in candidate_totals:
        errors.append("primary_monet_zone must name an impressionability candidate")
    for zone in secondary:
        if zone not in candidate_totals:
            errors.append(f"secondary Monet zone is not an impressionability candidate: {zone}")
    overlap = monet_zones.intersection(preserve)
    if overlap:
        errors.append("Monet zones cannot also be preserve_photo_zones: " + ", ".join(sorted(overlap)))
    if mode in {"atmospheric_monetization", "zine_hybrid"} and not preserve:
        errors.append(f"{mode} requires at least one preserved photo zone")
    if mode in {"full_impression", "subject_monetization", "distilled_monet"} and preserve:
        errors.append(f"{mode} cannot retain photo zones")

    if zine_strategy == "cutout_isolation":
        expected_plan = {
            "anchor_cutout",
            "monet_carrier_cutout",
            "anchor_treatment",
            "anchor_scope",
            "identity_lock",
            "recognition_features",
            "anchor_prominence",
            "anchor_long_axis_percent",
            "carrier_treatment",
            "carrier_evidence",
            "boundary_logic",
            "relation_to_preserve",
            "background_field",
            "quiet_area_percent",
            "discard_everything_else",
        }
        if not isinstance(zine_plan, dict) or set(zine_plan) != expected_plan:
            errors.append("zine_cutout_plan has missing or unsupported fields")
        else:
            for field in (
                "anchor_cutout",
                "monet_carrier_cutout",
                "anchor_scope",
                "carrier_evidence",
                "boundary_logic",
                "relation_to_preserve",
                "background_field",
            ):
                nonempty_string(zine_plan[field], f"zine_cutout_plan.{field}", errors)
            if zine_plan["anchor_treatment"] != "photographic":
                errors.append("zine_cutout_plan.anchor_treatment must be photographic")
            if zine_plan["identity_lock"] != "source_pixel_cutout":
                errors.append("zine_cutout_plan.identity_lock must be source_pixel_cutout")
            recognition = string_array(
                zine_plan["recognition_features"],
                "zine_cutout_plan.recognition_features",
                errors,
                min_items=3,
                max_items=8,
            )
            missing_protection = set(recognition) - set(protected)
            if missing_protection:
                errors.append(
                    "every recognition feature must also appear in protected_elements: "
                    + ", ".join(sorted(missing_protection))
                )
            if zine_plan["anchor_prominence"] not in {"primary", "balanced"}:
                errors.append("zine_cutout_plan.anchor_prominence must be primary or balanced")
            anchor_extent = zine_plan["anchor_long_axis_percent"]
            if (
                not isinstance(anchor_extent, int)
                or isinstance(anchor_extent, bool)
                or not 45 <= anchor_extent <= 80
            ):
                errors.append("zine_cutout_plan.anchor_long_axis_percent must be an integer from 45 to 80")
            if zine_plan["carrier_treatment"] != "monet_painted":
                errors.append("zine_cutout_plan.carrier_treatment must be monet_painted")
            if zine_plan["discard_everything_else"] is not True:
                errors.append("zine_cutout_plan.discard_everything_else must be true")
            plan_quiet = zine_plan["quiet_area_percent"]
            if not isinstance(plan_quiet, int) or isinstance(plan_quiet, bool) or not 30 <= plan_quiet <= 60:
                errors.append("zine_cutout_plan.quiet_area_percent must be an integer from 30 to 60")
            if len(preserve) != 1:
                errors.append("cutout_isolation requires exactly one preserve_photo_zone")
            elif zine_plan["anchor_cutout"] != preserve[0]:
                errors.append("zine_cutout_plan.anchor_cutout must exactly match the sole preserve_photo_zone")
            if zine_plan["monet_carrier_cutout"] != primary:
                errors.append("zine_cutout_plan.monet_carrier_cutout must exactly match primary_monet_zone")
            if isinstance(shape, dict) and isinstance(plan_quiet, int):
                if plan_quiet != shape.get("quiet_area_percent"):
                    errors.append("zine_cutout_plan.quiet_area_percent must equal shape_abstraction.quiet_area_percent")
        if secondary:
            errors.append("cutout_isolation does not allow secondary_monet_zones")
        if simplify_zones:
            errors.append("cutout_isolation does not allow simplify_zones")
        if line_zones:
            errors.append("cutout_isolation does not allow line_zones")
        if not negative_zones:
            errors.append("cutout_isolation requires a negative_space_zone for the removed remainder")
        if isinstance(shape, dict):
            if shape.get("primary_grammar") != "cutout":
                errors.append("cutout_isolation requires shape_abstraction.primary_grammar=cutout")
            if shape.get("supporting_grammar") is not None:
                errors.append("cutout_isolation requires shape_abstraction.supporting_grammar=null")

    override = data["primary_zone_override"]
    if not isinstance(override, str):
        errors.append("primary_zone_override must be a string; use an empty string when unused")
    elif candidate_totals and primary in candidate_totals:
        highest = max(candidate_totals.values())
        if candidate_totals[primary] < highest and not override.strip():
            errors.append("a lower-scoring primary Monet zone requires a recorded primary_zone_override")

    light = data["light_card"]
    required_light = {
        "direction",
        "temperature",
        "intensity",
        "diffusion",
        "time_or_condition",
        "surface_interactions",
        "highlight_family",
        "shadow_family",
        "reflection_relation",
    }
    if not isinstance(light, dict) or set(light) != required_light:
        errors.append("light_card has missing or unsupported fields")
    else:
        for field in required_light - {"surface_interactions"}:
            nonempty_string(light[field], f"light_card.{field}", errors)
        string_array(light["surface_interactions"], "light_card.surface_interactions", errors, min_items=1)

    palette = string_array(data["palette_families"], "palette_families", errors, min_items=5, max_items=9)
    if palette and not any("dark" in family.lower() or "shadow" in family.lower() for family in palette):
        warnings.append("palette_families does not explicitly name a chromatic dark or shadow role")

    brush_map = data["brush_map"]
    brush_zones: set[str] = set()
    if not isinstance(brush_map, list) or not brush_map:
        errors.append("brush_map must be a non-empty array")
    else:
        for index, brush in enumerate(brush_map):
            path = f"brush_map[{index}]"
            if not isinstance(brush, dict):
                errors.append(f"{path} must be an object")
                continue
            expected = {"zone", "primary_family", "supporting_family", "direction", "scale", "density"}
            if set(brush) != expected:
                errors.append(f"{path} has missing or unsupported fields")
                continue
            nonempty_string(brush["zone"], f"{path}.zone", errors)
            if brush["primary_family"] not in BRUSH_FAMILIES:
                errors.append(f"{path}.primary_family is invalid")
            if brush["supporting_family"] is not None and brush["supporting_family"] not in BRUSH_FAMILIES:
                errors.append(f"{path}.supporting_family is invalid")
            if brush["supporting_family"] == brush["primary_family"]:
                errors.append(f"{path} repeats the same primary and supporting family")
            for field in ("direction", "scale", "density"):
                nonempty_string(brush[field], f"{path}.{field}", errors)
            if isinstance(brush["zone"], str):
                brush_zones.add(brush["zone"])
    missing_brush = monet_zones - brush_zones
    if missing_brush:
        errors.append("every Monet zone needs a brush-map entry: " + ", ".join(sorted(missing_brush)))

    edge_map = data["edge_map"]
    levels: set[str] = set()
    if not isinstance(edge_map, list) or not edge_map:
        errors.append("edge_map must be a non-empty array")
    else:
        for index, edge in enumerate(edge_map):
            path = f"edge_map[{index}]"
            if not isinstance(edge, dict) or set(edge) != {"zone", "level", "reason"}:
                errors.append(f"{path} has missing or unsupported fields")
                continue
            nonempty_string(edge["zone"], f"{path}.zone", errors)
            nonempty_string(edge["reason"], f"{path}.reason", errors)
            if edge["level"] not in EDGE_LEVELS:
                errors.append(f"{path}.level is invalid")
            else:
                levels.add(edge["level"])
    if data["strength"] in {"M2", "M3", "M4"} and len(levels) < 2:
        errors.append("M2–M4 cards must use at least two edge levels")
    if mode in {"atmospheric_monetization", "zine_hybrid"} and "L1" not in levels:
        errors.append("partial-preservation modes need at least one L1 protected edge")

    if data["background_treatment"] not in BACKGROUNDS:
        errors.append("background_treatment is invalid")
    if data["transition_strategy"] not in TRANSITIONS:
        errors.append("transition_strategy is invalid")
    if data["transition_strategy"] == "torn_field" and mode != "zine_hybrid":
        errors.append("torn_field is allowed only in zine_hybrid")
    if data["background_treatment"] == "line" and not line_zones:
        warnings.append("line background selected without any line_zones")
    if data["background_treatment"] == "paper" and not negative_zones:
        warnings.append("paper background selected without any negative_space_zones")
    if zine_strategy == "cutout_isolation":
        if data["background_treatment"] != "paper":
            errors.append("cutout_isolation requires background_treatment=paper")
        if data["transition_strategy"] != "torn_field":
            errors.append("cutout_isolation requires transition_strategy=torn_field")

    composition = data["composition"]
    expected_composition = {"focal_order", "eye_path", "crop_ratio", "source_allocation"}
    if not isinstance(composition, dict) or set(composition) != expected_composition:
        errors.append("composition has missing or unsupported fields")
    else:
        string_array(composition["focal_order"], "composition.focal_order", errors, min_items=1)
        for field in ("eye_path", "crop_ratio", "source_allocation"):
            nonempty_string(composition[field], f"composition.{field}", errors)

    text = data["visible_text"]
    if not isinstance(text, str):
        errors.append("visible_text must be a string")
    elif len(text) > 80:
        errors.append("visible_text must be 80 characters or fewer")
    elif text and len(text.split()) > 4:
        warnings.append("visible_text exceeds the recommended four-word English title limit")
    if zine_strategy == "cutout_isolation" and text:
        errors.append("cutout_isolation requires visible_text to be empty by default")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("card", type=Path)
    parser.add_argument("--json", action="store_true", help="emit machine-readable validation output")
    args = parser.parse_args()

    try:
        data = json.loads(args.card.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    errors, warnings = validate(data)
    if args.json:
        print(json.dumps({"valid": not errors, "errors": errors, "warnings": warnings}, indent=2))
    else:
        for error in errors:
            print(f"ERROR: {error}")
        for warning in warnings:
            print(f"WARNING: {warning}")
        if not errors:
            print("VALID: Monet Transformation Card passed structural and mode checks")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
