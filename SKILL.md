---
name: monet-palette-photo
description: Transform a user-supplied photograph through source-responsive Monet-inspired color, light, brushwork, edge logic, and optional sparse social-media art direction. Route among full, subject-only, atmospheric, zine-hybrid, and distilled treatments; Zine Hybrid can preserve a prominent original-pixel anchor cutout beside one painted color-event cutout with controlled paper space. Optionally package the original and generated image as a warm comparison poster. Use for selective impressionist photo reinterpretation and social-ready image pairs, not generic oil-paint filters or invented Monet clichés.
---

# Monet-Palette-Photo

Create one art-directed transformation from a user-supplied photograph. Preserve the source's identity, semantic anchor, and spatial logic while deciding exactly where impressionist color and brush construction should appear. Treat transformation mode, presentation profile, and delivery layout as separate decisions.

## Core contract

- Treat the photograph as the sole factual source for people, objects, place, geometry, light evidence, and native color relationships.
- Route to exactly one transformation mode before prompting. Never blend incompatible source-pixel policies.
- Do not silently turn a selective request into a whole-image painting.
- Build an Impressionability Map before choosing painted zones. Evaluate light, atmosphere, reflection, color variation, and edge instability.
- Make palette, brush direction, edge behavior, and transition respond to the source. Do not apply one texture everywhere.
- When the `sparse_social` profile is active, extract a small set of source-derived shapes and leave deliberate quiet fields instead of filling the frame with paint or collage detail.
- When Zine Hybrid uses `cutout_isolation`, retain exactly one source-derived photographic anchor cutout and one source-derived Monet carrier cutout; keep 30–60% quiet paper and make the anchor the primary recognizable element.
- Preserve faces, hands, logos, architecture, and other protected anchors unless the selected mode explicitly transforms them.
- Never add water lilies, bridges, gardens, flowers, sunsets, period clothing, or other Monet-associated motifs unless they exist in the source or the user asks for them.
- Use one generation or edit pass, inspect the result when possible, and allow at most one targeted repair for a named QA failure.

## Route to one mode

Explicit mode names or decisive treatment instructions are authoritative. Otherwise read [references/mode-router.md](references/mode-router.md) and ask only the first unresolved routing question.

| Mode | Source pixels in result | Defining treatment | Detailed contract |
|---|---|---|---|
| Full Impression | None | Repaint the complete source while retaining scene identity and composition | [references/modes/full-impression.md](references/modes/full-impression.md) |
| Subject Monetization | None by default | Repaint the primary subject; reduce the rest to a deferential non-photographic field | [references/modes/subject-monetization.md](references/modes/subject-monetization.md) |
| Atmospheric Monetization | Partial, required | Keep the semantic anchor photographic; transform light, air, water, reflection, or unstable edges | [references/modes/atmospheric-monetization.md](references/modes/atmospheric-monetization.md) |
| Zine Hybrid | Partial, required | Combine truthful photo material, a Monet-inspired paint field, restrained paper, and optional linework | [references/modes/zine-hybrid.md](references/modes/zine-hybrid.md) |
| Distilled Monet | None | Use the source as semantic and structural evidence for a freer, potentially abstract painting | [references/modes/distilled-monet.md](references/modes/distilled-monet.md) |

Do not default to Full Impression for a generic request such as “make this Monet.” Clarify the intended source-pixel policy and treatment first.

## Select a presentation profile

Presentation profile controls visual density without changing the mode's source-pixel contract.

- `immersive`: retain the mode's existing full-field visual behavior.
- `sparse_social`: prioritize thumbnail clarity, one source-derived graphic grammar, one dominant active cluster, and generous blank or low-information fields. Read [references/sparse-social.md](references/sparse-social.md).

Explicit requests for social-media clarity, minimalism, abstraction, extracted shapes, negative space, or zine-like reduction select `sparse_social`. Otherwise use the profile defaults in [references/mode-router.md](references/mode-router.md). Do not ask about the profile when the request or mode supplies a safe default.

## Select a Zine strategy

This decision applies only to Zine Hybrid:

- `integrated_field`: the existing default—one photographic anchor, one Monet paint event, and optional restrained paper or line support remain integrated as a sparse scene.
- `cutout_isolation`: keep exactly two source-derived cutouts on quiet paper: a truthful photographic anchor and a separately bounded Monet-painted carrier. Read [references/zine-cutout-isolation.md](references/zine-cutout-isolation.md).

Explicit instructions such as “cut out the anchor and the Monet carrier,” “keep only those two regions,” “remove the rest,” “双剪纸,” or “其余全部留白” select `cutout_isolation`. A generic Zine Hybrid request keeps the backward-compatible `integrated_field` default.

## Select a delivery layout

Delivery layout is independent of the generated artwork:

- `artwork_only` is the default.
- `comparison_poster` places the truthful original above the generated artwork on a warm source-derived background with visible space around and between both panels. Read [references/comparison-poster.md](references/comparison-poster.md) only when requested.

Words such as “comparison poster,” “before/after,” “original on top,” “画报,” or “原图在上、生成图在下” select `comparison_poster`. The poster compositor must not re-render either panel.

## Workflow

1. Require a user-supplied photograph. Inspect it directly; do not browse for substitute imagery.
2. Route to one mode and one presentation profile. For Zine Hybrid, also resolve one Zine strategy; read [references/zine-cutout-isolation.md](references/zine-cutout-isolation.md) only when that strategy is selected. Read only the selected mode reference and, for `sparse_social`, [references/sparse-social.md](references/sparse-social.md). Confirm mode, strength, profile, and applicable Zine strategy in one sentence.
3. Read [references/transformation-card.md](references/transformation-card.md). Build a compact JSON Monet Transformation Card and validate it with `scripts/validate_transformation_card.py`.
4. Read [references/visual-system.md](references/visual-system.md), then load [references/palette-engine.md](references/palette-engine.md) and [references/brush-light-edge.md](references/brush-light-edge.md) only for the fields used by the selected mode and profile.
5. Read [references/prompt-compiler.md](references/prompt-compiler.md). Compile one English render prompt from the validated card. Keep analysis, scores, file paths, and provenance out of the prompt.
6. Use the host's available reference-image generation or editing tool. Pass the source image as a reference; use a mask or deterministic compositing when exact pixel preservation is required and supported. For `cutout_isolation`, run the Subject Integrity Gate in [references/zine-cutout-isolation.md](references/zine-cutout-isolation.md): extract and composite the photographic anchor from original source pixels after generating the carrier and paper whenever deterministic compositing is available.
7. Inspect the artwork against [references/qa.md](references/qa.md). If one concrete check fails, change only the corresponding repair dimension and retry at most once.
8. If `comparison_poster` is requested, build a Social Output Card from [references/social-output-card.schema.json](references/social-output-card.schema.json), then run `scripts/compose_comparison_poster.py` with the original and accepted artwork. Inspect the composed poster against the delivery QA in [references/comparison-poster.md](references/comparison-poster.md). Do not send the panels through another generative pass.
9. Return the requested artwork or poster, selected mode, strength, presentation profile, and one concise rationale. Show prompts or cards only when requested.

Consult [references/blueprint.json](references/blueprint.json) for the complete design decisions, source authority, defaults, and provenance. Use [references/examples.md](references/examples.md) only to understand card structure; never reuse example content as a visual default.

## Clarification policy

- Ask one concise routing question at a time only when the request leaves materially incompatible modes possible.
- Do not ask about palette, brush family, edge level, or ratio when the source and mode provide a safe default.
- Use source orientation by default. Use strength defaults from the selected mode unless the user specifies `M1`, `M2`, `M3`, or `M4`.
- Use `artwork_only` unless the user asks for a comparison or poster layout. For `comparison_poster`, default to a moderate-resolution `4:5` canvas, contained panels, no labels, and source-derived warm background.
- Use no visible text by default. If the user supplies text, reproduce it exactly; keep it to one short title or caption. For production-critical spelling, composite text deterministically.
- If the required editing or masking capability is unavailable, return the complete prompt package and explain the fidelity limitation instead of claiming a finished transformation.
- For `cutout_isolation`, ask one concise question when the photographic anchor and Monet carrier cannot be separated into two traceable source regions. Do not invent a decorative blob or silently merge the two roles.
- If `cutout_isolation` cannot retain the anchor through an original-pixel cutout, ask whether best-effort generative identity preservation is acceptable; otherwise return the prompt and mask plan. Never describe a regenerated likeness as a preserved photographic subject.

## Source handling

- Do not save, search, publish, or send the source to unrelated services.
- Send only the final prompt and required source image to the configured generation/editing service.
- When a source image is sent to such a service, disclose that briefly after generation.

## Output

Default:

1. One generated or edited raster image.
2. `Mode: <mode> · Strength: <M1–M4> · Profile: <immersive|sparse_social>`; append `· Zine: <integrated_field|cutout_isolation>` for Zine Hybrid.
3. One short rationale naming the chosen Monet zones and the decisive light/color/edge relationship.

When `comparison_poster` is requested, return the composed poster as the primary deliverable and state that the top panel is the original and the bottom panel is the generated artwork.

On request, also provide the validated transformation card, final prompt, palette recipe, or targeted revision notes.
