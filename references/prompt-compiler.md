# Prompt compiler

Compile one English render prompt from a validated Monet Transformation Card. Keep the card, prompt, and tool parameters separate.

## Field order

1. **Task and medium** — state the selected mode, strength, presentation profile, applicable Zine strategy, final image orientation, and whether the result is a complete painting, selective edit, or flat hybrid artwork.
2. **Source fidelity** — name the semantic anchor, protected elements, spatial invariants, and source-pixel policy.
3. **Transformation map** — state the primary and secondary Monet zones, preserved zones, simplified/line/paper zones, and discard list.
4. **Light interpretation** — direction, temperature, diffusion, intensity, surface interaction, highlights, chromatic shadows, and reflection relation.
5. **Palette construction** — five to nine source-responsive color families or roles for principal Monet zones.
6. **Brush map** — primary family, direction, scale, and density per painted zone; relate it to surface, depth, and light.
7. **Edge hierarchy** — list L1 protected edges and the L2–L4 transitions that create atmosphere or reflection.
8. **Transition strategy** — one source-derived boundary behavior.
9. **Background treatment** — preserve, simplify, line, or paper; state how it defers.
10. **Sparse shape system** — only for `sparse_social`: semantic minimum, one primary graphic grammar, retain/merge/omit/transform/expose decisions, dominant active cluster, quiet fields, and thumbnail anchor.
11. **Cutout isolation** — only for `cutout_isolation`: exact anchor scope, source-pixel identity lock, recognition features, primary scale, carrier boundary, surviving source relation, one cut-edge system, 30–60% quiet paper, and removal of everything else.
12. **Composition** — focal order, eye path, crop, negative space, and relationship between factual anchor and painted event.
13. **Typography** — exact short text or explicitly no text.
14. **Material and hard avoids** — matte painterly behavior, flat presentation, mode-specific negatives, and no invented motifs.

Omit irrelevant fields. Do not copy field labels, scores, JSON, file paths, analysis commentary, or provenance into the render prompt.

## Prompt construction rules

- Use source-specific nouns and relationships. Replace “beautiful Monet atmosphere” with the observed light, reflective surface, palette relation, brush direction, and edge behavior.
- Name every preserved zone before describing paint. In partial modes, repeat the preservation boundary once in the hard constraints.
- Use one primary brush family per zone and at most one supporting family.
- Keep the palette relational: dominant, light, warm/cool counter, reflection, and chromatic dark. Do not output a disconnected swatch list.
- State exact visible text once. If `visible_text` is empty, require no typography, labels, watermarks, signatures, or invented metadata.
- Do not ask the model to preserve and repaint the same pixels. Resolve overlaps in the card first.
- For `sparse_social`, describe visible density and shape relationships rather than dumping percentage values or card terminology. State what remains quiet as firmly as what becomes active.
- For `cutout_isolation`, describe exactly two source-derived pieces. Do not include scene-wide paint, background atmosphere, secondary marks, line support, or any language that could preserve the discarded scenery.
- Name the anchor first and state that its original photographic pixels must be composited unchanged. Require primary or balanced visual prominence and forbid facial, anatomical, wardrobe, pose, texture, or structural drift.
- Keep `comparison_poster` out of the generation prompt. It is a deterministic post-generation layout, not part of the artwork.

## Render-prompt skeleton

```text
Create a [MODE] transformation at [STRENGTH], preserving the source orientation.

SOURCE FIDELITY
[semantic anchor, protected elements, spatial invariants, source-pixel policy]

TRANSFORMATION MAP
[primary/secondary Monet zones, preserved and reduced zones, discard]

LIGHT
[direction, temperature, diffusion, interaction, highlight and chromatic-shadow families]

PALETTE
[source-responsive families and their structural roles]

BRUSH
[zone-specific family, direction, scale, density, and depth behavior]

EDGES AND TRANSITION
[L1–L4 map and one source-derived transition]

BACKGROUND AND COMPOSITION
[deferential treatment, focal order, eye path, negative space]

SPARSE SHAPE SYSTEM (only when selected)
[semantic minimum, primary grammar, retain/merge/omit/transform/expose, active cluster, quiet fields, thumbnail anchor]

CUTOUT ISOLATION (only when selected)
[original-pixel anchor cutout, recognition features and primary scale, one painted carrier cutout, source relation, boundary logic, 30–60% quiet paper, remove everything else]

TEXT
[exact short text, or no visible text]

HARD CONSTRAINTS
[mode-specific preservation, selectivity, no filter, no black-shadow default, no invented Monet motifs]
```

## Tool-call contract

- Inspect the supplied image before building the card.
- Use a reference-image generation or editing tool.
- Map source image, optional mask, aspect ratio, and output count to tool parameters rather than descriptive prose.
- Generate one result by default.
- For Atmospheric Monetization and Zine Hybrid, prefer regional editing, a mask, or deterministic compositing. If unavailable, do not claim pixel-exact preservation.
- For `cutout_isolation`, use two non-overlapping source-derived masks: one original-pixel photographic anchor mask and one painted carrier mask. Generate the carrier/paper layer first when necessary, then composite the unchanged anchor above it. The inverse of both masks becomes paper, not a simplified scene.
- If the available tool cannot preserve or composite the source-pixel anchor, do not claim completion under the strict contract; ask for best-effort permission or return the prompt and mask plan.
- When exact short text matters, generate the artwork without text and add it deterministically.
- If generation is unavailable, return the compiled prompt, mask/zone plan, and parameters as the honest fallback.
- If `comparison_poster` is requested, generate and approve the artwork first, then compose the original and result with `scripts/compose_comparison_poster.py`. Never ask the generation tool to draw the two-panel poster.

## Correction prompt

When QA fails, retain the accepted card and rewrite only one dimension:

- source fidelity, subject recognition, or mask spill;
- mode/selectivity;
- palette or chromatic darks;
- brush direction/scale;
- edge hierarchy;
- transition boundary;
- background hierarchy;
- sparse density or thumbnail clarity;
- cutout count, cutout provenance, or discarded-background leakage;
- text rendering.

Do not change the subject, mode, crop, and palette together unless the user requests a new direction.
