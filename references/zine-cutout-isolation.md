# Zine Cutout Isolation

Use this strategy only inside Zine Hybrid when the user wants a stronger zine reduction: isolate the photographic anchor and the principal carrier of the Monet color event as two source-derived paper cutouts, then remove the rest of the scene.

## Identity

The result is a sparse two-piece visual sentence:

1. one immediately recognizable photographic anchor cutout with primary visual weight;
2. one Monet-painted carrier cutout;
3. an otherwise quiet paper field.

This is not a full-scene collage, a decorative scrapbook, or a painting with a torn-paper overlay. Blank paper is an active compositional region.

## Source contract

- The source photograph is the sole factual and geometric authority.
- The anchor cutout must exactly follow a recognizable source region that carries the scene's semantic identity.
- The carrier cutout must exactly follow a separately traceable source region with the strongest light, atmosphere, reflection, color variation, or edge instability.
- Preserve one decisive source relationship between the two cutouts: gaze, axis, overlap, distance, above/below order, directional light, or reflection relation.
- The anchor remains photographic. The carrier becomes Monet-inspired paint.
- Delete all other source regions. Do not simplify, redraw, haze, or decorate them.
- Never add a cutout, hole, color patch, object, or motif that cannot be traced to source evidence.

## Selection procedure

1. Name the semantic minimum and choose one photographic anchor.
2. Rank the Impressionability Map. Select the highest-scoring separable region as the carrier; record a source-specific reason if a semantic override is necessary.
3. Confirm that the two regions have distinct, defensible boundaries and do not overlap.
4. Choose one relation that must survive when the background disappears.
5. Record both regions in `zine_cutout_plan`; remove every unselected region to paper.

If the anchor and carrier are the same object, overlap materially, or cannot be bounded without guessing, ask one concise question before generation. Offer the user a choice between selecting a different carrier and returning to `integrated_field`. Do not silently duplicate, split, or invent a region.

## Subject Integrity Gate

Resolve the anchor before generating anything:

1. Define `anchor_scope` to include the complete identity-bearing subject, its attached belongings, and an optional narrow contact patch when that patch is necessary to keep pose or grounding legible.
2. Record three to eight `recognition_features`, prioritizing face, hair, glasses, hands, pose, clothing pattern, object silhouette, signage, or architecture as applicable.
3. Give the anchor primary prominence. Its longest visible axis should normally occupy 45–80% of the frame dimension that best supports recognition.
4. Use an original-source-pixel mask and deterministic composite whenever available. Generate or paint the carrier and paper separately, then place the unchanged anchor cutout above them.
5. Do not ask a generative model to recreate the anchor when exact identity matters. If deterministic extraction is unavailable, ask whether best-effort generative preservation is acceptable or return the mask plan.

The anchor may be repositioned or uniformly scaled for composition, but do not alter its face, anatomy, pose, clothing, internal photographic texture, or attached identity-bearing details. Do not crop through the head, hands, feet, signature silhouette, or relevant attached objects.

## Shape and material rules

- `presentation_profile`: `sparse_social`.
- `primary_grammar`: `cutout`.
- `supporting_grammar`: `null`.
- Keep exactly two active cutouts. Internal source detail may remain inside the photographic anchor; it does not count as extra collage pieces.
- Use one consistent torn-or-cut boundary language across both pieces. Let contours derive from the selected source regions rather than generic rectangles or circles.
- Keep paper matte, flat, and lightly tactile. Avoid drop shadows, curled paper, tape, staples, stickers, frames, or three-dimensional scrapbook depth.
- Allow 30–60% quiet paper and approximately 35–65% combined active shape area. Keep enough paper to separate the two pieces, but do not let emptiness overwhelm the subject.
- Keep the anchor visually primary or balanced with the carrier; never let the carrier reduce it to a minor sticker.
- Let the carrier expand, bend, or wrap through the source-derived axis to reduce dead space while remaining one continuous cutout.
- Use a restrained warm or source-derived neutral paper field unless the user specifies another background.
- Use no visible text; keep any caption outside the artwork or add it later in a separate delivery layout.

## Paint behavior

Paint only inside the carrier cutout. Build its color and brush direction from the observed light, surface, reflection, atmosphere, and local palette. Keep the photographic anchor free of painterly spill. Do not fill the paper field with atmospheric brushwork.

At M2–M4, keep at least two edge levels inside the painted carrier while preserving the carrier silhouette as a readable cut boundary. The anchor boundary and any protected face, hand, identity feature, or architecture use L1 where required.

## Prompt behavior

State these constraints in this order:

1. the exact photographic anchor scope, source-pixel identity lock, recognition features, and primary scale;
2. the exact Monet carrier cutout and its source evidence;
3. the source relation between them;
4. the single boundary system;
5. the instruction to remove every other region to quiet paper;
6. the prohibition on extra scraps, linework, scenery, text, and invented motifs.

Do not describe the discarded background as a faint painting, simplified landscape, atmospheric extension, or collage support. It must be absent.

## QA

- [ ] Exactly two active cutouts remain.
- [ ] One cutout uses original photographic subject pixels and one is Monet-inspired paint.
- [ ] The complete anchor and its defining recognition features match the source without facial, anatomical, wardrobe, or structural drift.
- [ ] The anchor is the primary recognizable element at thumbnail size and is not cropped into an anonymous fragment.
- [ ] Both boundaries are traceable to distinct source regions.
- [ ] One decisive source relationship survives between the two pieces.
- [ ] All other scenery is absent, not faded or redrawn.
- [ ] Quiet paper occupies 30–60% of the frame and does not overwhelm the two active pieces.
- [ ] No supporting grammar, extra scrap, filler mark, text, or invented motif appears.
- [ ] Paint does not spill into the photographic anchor or paper field.
