# Brush, light, and edge grammar

Brush behavior must follow surface orientation, spatial depth, and light condition. Edge behavior must follow semantic importance and atmospheric interference.

## Brush families

### Broken dabs

Use for flowers, foliage, scattered highlights, small distant figures, and fragmented color events. Keep size and spacing irregular but source-directed.

### Short directional strokes

Use for grass, sky bands, architectural planes, fabric, and moving surfaces. Align strokes to the surface or dominant visual flow.

### Horizontal shimmer

Use for water, wet ground, or low horizontal reflections. Break the bands; do not produce uniform stripes.

### Vertical veil

Use for hanging foliage, rain, tall reflections, reeds, or downward atmospheric movement. Keep the direction tied to the source.

### Broad flat patches

Use for large planes of water, grass, sky, wall, or distant architecture. At M3–M4, allow patches to simplify local detail while preserving value and spatial function.

### Feathered atmosphere

Use for haze, fog, sky diffusion, distant trees, and lost forms. Keep contrast and chroma lower than nearer painted zones unless the source light creates a deliberate flare.

Choose one primary family per zone and at most one supporting family. Do not list all brush types in every prompt.

In `sparse_social`, concentrate visible brush density inside the active cluster. Quiet fields may use broad flat patches, feathered atmosphere, calm unmarked paper, or low-density strokes as permitted by the mode. Do not miniaturize dense source texture across the entire frame.

## Spatial scale

- foreground: larger, more visible, and more material-specific strokes;
- midground: medium broken or directional strokes;
- background: smaller, softer, lower-contrast strokes;
- atmosphere: merged or feathered passages with selective edge loss.

The same brush texture must not cover every depth layer.

## Light-to-brush mapping

- direct light: shorter, higher-contrast, higher-chroma marks where the source supports them;
- diffuse fog or overcast light: layered feathered marks and compressed contrast;
- water reflection: broken horizontal repetition with color from sky and environment;
- dappled light: scattered small marks with warm/cool variation;
- reflected glow: softer directional passages that follow the receiving surface.

Light changes both palette and brush behavior. If the two systems disagree, correct the brush map rather than adding generic texture.

## Edge hierarchy

- **L1 — Defined:** semantic anchor, essential identity feature, or protected geometry.
- **L2 — Soft:** important form with atmosphere or paint transition.
- **L3 — Broken:** secondary subject, foliage, moving contour, or interrupted light.
- **L4 — Lost:** reflection, mist, glare, distant form, or deliberate dissolution.

Use at least two edge levels in M2–M4. Do not blur every edge. In partial-preservation modes, the transformation boundary must not degrade L1 protected elements.

## Transition boundary

Describe the boundary as a source event:

- brush follows a real contour or light footprint;
- color breaks along an observed reflection or surface change;
- edge certainty decreases with distance or atmosphere;
- zine tearing follows a source-derived axis and remains subordinate.

Avoid hard digital splits, generic gradients, halos around people, and arbitrary paint splashes.
