# Mode router

Select exactly one mode and one presentation profile before building the transformation card. Mode controls source-pixel retention and transformation scope. Presentation profile controls density and negative space. Explicit names and explicit source-pixel instructions win over inference.

## Decision order

1. **Explicit mode** — use it unchanged unless it conflicts with a required input.
2. **Decisive treatment**:
   - “paint/repaint the whole photo” selects Full Impression;
   - “paint only the person/object/subject” selects Subject Monetization;
   - “keep the person/photo real; paint the light, air, water, reflection, or background” selects Atmospheric Monetization;
   - “photo plus paper, linework, collage, or zine” selects Zine Hybrid;
   - “do not retain the photo; distill/recompose/abstract it” selects Distilled Monet.
3. **Ambiguous request** — ask the first unresolved question below and stop as soon as the mode is certain.

## Guided routing questions

First ask:

> Should any original photographic pixels remain visible in the final artwork?

- **Yes** — distinguish Atmospheric Monetization from Zine Hybrid:
  > Should the painted transition follow natural light/air/reflection, or should it become a paper-and-line zine composition?
- **No** — distinguish the three repainting modes:
  > Should the whole scene be repainted, only the main subject be painted, or should the source be freely distilled into a new composition?

If the user says “you decide,” choose the mode best supported by the requested treatment. Do not interpret this as permission to erase source pixels when the request emphasizes preservation.

## Required inputs

All modes require a source photograph. Atmospheric Monetization and Zine Hybrid additionally require a tool path capable of retaining or recombining source pixels. If that capability is unavailable, preserve the selected mode and return a prompt/mask plan; do not fall back to a different mode.

## Strength defaults

| Mode | Default | Rationale |
|---|---|---|
| Full Impression | M3 | Complete brush construction without late-period dissolution |
| Subject Monetization | M3 | Painted subject must read clearly against a reduced field |
| Atmospheric Monetization | M2 | Selective broken color and lost edges should not erase the anchor |
| Zine Hybrid | M2 | Paint supports the photo/paper system rather than taking it over |
| Distilled Monet | M4 | Freer surface rhythm and spatial uncertainty are intentional |

Strength is optional. Use the default without asking unless the user requests more or less transformation.

## Triggered strategies

Light-triggered and Reflection-triggered Monetization are strategies inside Atmospheric Monetization:

- **Light-triggered** — painted zones follow the dominant light footprint and its spill across surfaces.
- **Reflection-triggered** — the real subject remains photographic while its reflection or reflective environment becomes painted.

They are not separate top-level modes because they share the same partial-preservation contract.

## Presentation-profile routing

Apply this after mode selection:

1. Explicit `immersive` or `sparse_social` wins.
2. Requests for social-media clarity, thumbnail legibility, minimalism, distilled shapes, graphic extraction, more negative space, less visual fatigue, or zine-like reduction select `sparse_social`.
3. Requests to fill or repaint the whole frame, preserve dense environmental detail, or create an immersive painting select `immersive`.
4. When unspecified, use:

| Mode | Default profile |
|---|---|
| Full Impression | `immersive` |
| Subject Monetization | `sparse_social` |
| Atmospheric Monetization | `immersive` |
| Zine Hybrid | `sparse_social` |
| Distilled Monet | `sparse_social` |

Do not ask about the profile unless the user combines materially conflicting cues. `sparse_social` never overrides the selected mode's source-pixel policy: a Full or Distilled result still contains no photographic pixels, while Atmospheric and Zine Hybrid still retain truthful photo regions.

## Delivery-layout routing

Use `artwork_only` by default. Select `comparison_poster` when the user asks for a poster, before/after card, original-over-result layout, “画报,” or equivalent. Delivery layout is a post-generation composition decision; it must not affect which source pixels are retained inside the generated artwork.
