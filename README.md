[English](README.md) | [简体中文](README.zh-CN.md)

# Monet-Palette-Photo

Transform a source photograph through Monet-inspired color, light, brushwork, and edge logic while preserving its subject and spatial relationships.

This is an art-direction skill, not a generic oil-paint filter. The photograph remains the factual source for subjects, geometry, light, and palette.

## Modes

| Mode | Treatment |
|---|---|
| Full Impression | Repaint the complete photograph. |
| Subject Monetization | Paint the main subject and reduce its context. |
| Atmospheric Monetization | Preserve a photographic anchor; paint atmosphere, water, reflections, or light. |
| Zine Hybrid | Combine a photographic anchor with a Monet-painted field. |
| Distilled Monet | Rebuild the scene as a freer, source-derived painting. |

Strength ranges from `M1` (subtle) to `M4` (abstract). Use `Sparse Social` for simpler shapes, lower density, and stronger thumbnail readability.

## Zine Hybrid strategies

- `Integrated Field`: a photographic anchor remains embedded in a full painted or simplified environment.
- `Cutout Isolation`: one photographic anchor and one painted carrier remain on 30–60% quiet paper.

Optional `Comparison Poster` output places the original above the generated artwork on a warm 4:5 canvas.

## Example requests

```text
Use Monet-Palette-Photo with Atmospheric Monetization · M2.
Keep the building photographic and transform the sky, mountains, and water.
```

```text
Use Zine Hybrid · M3 · Sparse Social · Integrated Field.
Preserve the person as the photographic anchor and paint the remaining scene.
```

```text
Use Zine Hybrid · M2 · Cutout Isolation with about 40% quiet paper.
```

## Notes

- No visible text is added unless requested.
- The skill avoids invented Monet motifs unsupported by the source.
- Exact source-pixel retention requires deterministic masks or compositing. Generative-only editing provides best-effort preservation and must not be described as pixel-exact.

See [SKILL.md](SKILL.md) for the full workflow and [references/](references/) for mode contracts, schemas, prompting, and QA.
