# Monet Transformation Card

Build this card after selecting a mode and before writing the render prompt. Save it as temporary JSON when running the validator; do not persist the user's source path or image unless the user asks.

The canonical structure is [transformation-card.schema.json](transformation-card.schema.json).

## Required fields

### Routing

- `mode`: one selected mode.
- `strength`: `M1`, `M2`, `M3`, or `M4`.
- `presentation_profile`: `immersive` or `sparse_social`.
- `shape_abstraction`: `null` for `immersive`; a complete Shape Extraction Card for `sparse_social`.
- `zine_strategy`: `not_applicable`, `integrated_field`, or `cutout_isolation`.
- `zine_cutout_plan`: `null` except for `cutout_isolation`; then a complete two-cutout plan.
- `source_pixel_policy`: `none_retained` or `partial_required`, consistent with the selected mode.
- `source_orientation`: `portrait`, `landscape`, or `square`.

### Source anchors

- `semantic_anchor`: the subject or relationship that makes the source meaningful.
- `primary_subject`: one main subject, or two inseparable subjects.
- `supporting_elements`: one to three elements that establish place, action, or atmosphere.
- `spatial_invariants`: relative position, scale, direction, horizon, gaze, path, overlap, reflection axis, or silhouette that must survive.
- `protected_elements`: faces, hands, logos, identity features, text, or architecture that must not drift.
- `discard`: clutter, irrelevant detail, and forbidden invented motifs.

### Impressionability candidates

For each candidate zone, record:

- zone name;
- scores from 0–4 for `light`, `atmosphere`, `reflection`, `color_variation`, and `edge_instability`;
- `total`, equal to the five scores;
- one source-specific rationale.

Select:

- `primary_monet_zone`;
- zero to two `secondary_monet_zones` that support the same perceptual event;
- `preserve_photo_zones`;
- `simplify_zones`;
- `line_zones`;
- `negative_space_zones`.

Do not assign one region to both `primary_monet_zone` and `preserve_photo_zones`. In partial-preservation modes, preserve at least one meaningful photographic zone.

### Light Card

- `direction`;
- `temperature`;
- `intensity`;
- `diffusion`;
- `time_or_condition`;
- `surface_interactions`;
- `highlight_family`;
- `shadow_family`;
- `reflection_relation`.

If a property cannot be observed, use `uncertain` and avoid inventing precision.

### Art-direction systems

- `palette_families`: five to nine named color families or roles for each principal Monet zone.
- `brush_map`: zone, primary brush family, direction, scale, and density.
- `edge_map`: zone and edge level `L1`–`L4`.
- `background_treatment`: `preserve`, `simplify`, `line`, or `paper`.
- `transition_strategy`: one allowed transition.
- `composition`: focal order, eye path, crop/ratio, and source allocation.
- `visible_text`: exact short copy or an empty string.

### Sparse Social fields

When `presentation_profile` is `sparse_social`, read [sparse-social.md](sparse-social.md) and complete:

- semantic minimum and dominant gesture;
- one or two source-shape candidates;
- retain, merge, omit, transform, and expose actions;
- one primary graphic grammar and zero or one supporting grammar;
- detail-removal, quiet-area, and active-shape budgets;
- one thumbnail anchor.

For `immersive`, set `shape_abstraction` to `null`. The profile changes density only; mode remains authoritative for source-pixel retention.

### Zine Cutout Isolation fields

When `mode` is `zine_hybrid` and `zine_strategy` is `cutout_isolation`, read [zine-cutout-isolation.md](zine-cutout-isolation.md) and complete:

- `anchor_cutout`: exactly the sole entry in `preserve_photo_zones`;
- `monet_carrier_cutout`: exactly `primary_monet_zone`;
- `anchor_treatment`: `photographic`;
- `anchor_scope`: the complete identity-bearing subject, attached belongings, and any essential contact patch;
- `identity_lock`: `source_pixel_cutout`;
- `recognition_features`: three to eight source features that must remain exact;
- `anchor_prominence`: `primary` or `balanced`;
- `anchor_long_axis_percent`: 45–80, describing the intended longest on-canvas anchor dimension;
- `carrier_treatment`: `monet_painted`;
- `carrier_evidence`: the observed reason this region carries the Monet event;
- `boundary_logic`: how both cutout boundaries derive from their source regions;
- `relation_to_preserve`: one source spatial or perceptual relation between the cutouts;
- `background_field`: the quiet paper color/material direction;
- `quiet_area_percent`: 30–60 and equal to `shape_abstraction.quiet_area_percent`;
- `discard_everything_else`: `true`.

This strategy also requires `sparse_social`, `primary_grammar=cutout`, no supporting grammar, 35–65% active shape area, `background_treatment=paper`, `transition_strategy=torn_field`, exactly one preserved photo zone, no secondary Monet zones, no simplify or line zones, and at least one negative-space zone naming the removed remainder.

For Zine Hybrid's normal sparse scene, use `zine_strategy=integrated_field` and `zine_cutout_plan=null`. For every non-Zine mode, use `zine_strategy=not_applicable` and `zine_cutout_plan=null`.

## Validation

Run:

```bash
python3 scripts/validate_transformation_card.py /path/to/card.json
```

The validator checks structure, score totals, mode/source-pixel compatibility, zone collisions, palette size, edge levels, transitions, profile-dependent shape extraction, density budgets, Zine strategy invariants, and retry-independent constraints. Passing validation does not prove aesthetic success; use visual QA after generation.
