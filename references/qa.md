# Monet authenticity and delivery QA

Run preflight before generation and visual QA on the actual result when it can be inspected. If inspection is unavailable, mark result QA as unverified.

## Preflight

- [ ] Exactly one mode is selected.
- [ ] Exactly one presentation profile is selected.
- [ ] Mode and source-pixel policy are compatible.
- [ ] A supplied photograph is available and has been inspected.
- [ ] Semantic anchor, protected elements, and spatial invariants are explicit.
- [ ] The primary Monet zone comes from the Impressionability Map or has a recorded semantic override.
- [ ] Monet zones do not overlap preserved photo zones.
- [ ] The Light Card is based on observed evidence; uncertain values are labeled.
- [ ] Palette roles, brush map, edge levels, background, and transition are resolved.
- [ ] No protected element is assigned to a destructive transition without explicit user intent.
- [ ] Visible text is exact and short, or explicitly absent.
- [ ] The Transformation Card passes `scripts/validate_transformation_card.py`.
- [ ] For `sparse_social`, the Shape Extraction Card resolves one primary grammar, a thumbnail anchor, quiet fields, and density budgets.

## Visual QA

### Source and selectivity

- [ ] The semantic anchor and decisive spatial relationship remain readable.
- [ ] Only planned zones were transformed.
- [ ] Partial-preservation modes retain truthful photo pixels without stylistic spill.
- [ ] Full, Subject, and Distilled modes contain no accidental photographic fragments.
- [ ] No unrequested object, scenery, weather, reflection, or Monet-associated motif was introduced.

### Light and color

- [ ] Light changes local color and agrees with the observed direction and diffusion.
- [ ] Shadows remain chromatic rather than defaulting to flat black or gray.
- [ ] Principal Monet zones contain purposeful warm/cool variation.
- [ ] Water and reflective surfaces use sky, environment, reflected subject, and local surface color rather than generic blue.
- [ ] The result has not been reduced to a universal pastel palette.

### Brush and depth

- [ ] Brush direction follows surface, motion, reflection, or atmosphere.
- [ ] Different materials and depth layers do not share one uniform filter texture.
- [ ] Foreground, midground, background, and atmosphere use appropriate scale and contrast.
- [ ] Impasto or grain is selective and does not obscure protected identity.

### Edges and transition

- [ ] At least two edge levels are visible at M2–M4.
- [ ] L1 protected edges remain stable where required.
- [ ] Reflection, mist, glare, or distance uses broken or lost edges where planned.
- [ ] The photo-to-paint transition follows source light, geometry, or reflection rather than a hard digital split or generic gradient.

### Composition and hierarchy

- [ ] One semantic anchor and one dominant painted event organize the image.
- [ ] Background, paper, linework, and typography defer to the anchor and paint.
- [ ] Zine Hybrid remains flat and restrained rather than becoming a dense scrapbook or commercial poster.
- [ ] Any visible title is exact, legible enough for its role, and free of invented metadata.

### Sparse Social

Apply only when `presentation_profile=sparse_social`:

- [ ] The semantic minimum remains legible at roughly one-quarter display size.
- [ ] One source-derived graphic grammar dominates; any supporting grammar remains subordinate.
- [ ] One active cluster and no more than two support marks organize the frame.
- [ ] Blank or low-information fields create real breathing room rather than accidental emptiness.
- [ ] Dense source detail has been merged or omitted instead of redrawn at smaller scale.
- [ ] Quiet fields do not accumulate filler marks, captions, stickers, or unrelated collage devices.

### Comparison Poster

Apply only after composing `comparison_poster`:

- [ ] The original appears above and the generated artwork below.
- [ ] Neither panel was regenerated, retouched, or silently cropped during layout.
- [ ] Warm background remains visible around all sides and between panels.
- [ ] The background color is source-derived or exactly user-specified and remains subordinate.
- [ ] The poster contains no invented labels, metadata, shadows, tape, or props.

## Failure labels and repair

Use one label:

- `source_fidelity`
- `mask_spill`
- `mode_selectivity`
- `palette_relation`
- `chromatic_shadows`
- `brush_logic`
- `edge_hierarchy`
- `transition_boundary`
- `background_hierarchy`
- `sparse_density`
- `thumbnail_clarity`
- `poster_layout`
- `text_rendering`

Keep all accepted decisions fixed and repair only the failed dimension. Allow one automatic targeted retry. If it still fails, return the best result plus the named limitation and wait for user direction.

## Delivery

Return:

1. the generated image, or the composed comparison poster when requested;
2. selected mode, strength, and presentation profile;
3. one concise rationale naming the Monet zones and decisive perceptual relationship;
4. a brief external-service disclosure when the source image was sent to the configured generation/editing service.

If returning a comparison poster, state that the top panel is the untouched original and the bottom panel is the accepted generated artwork.

Show the prompt, card, palette families, or detailed QA only when requested.
