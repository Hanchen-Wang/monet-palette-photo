# Comparison Poster delivery layout

Use this only after the generated artwork has passed visual QA. It packages two accepted raster images; it does not generate or restyle either panel.

## Output contract

- Top panel: the truthful user-supplied original photograph.
- Bottom panel: the accepted Monet-Palette-Photo result.
- Background: a quiet warm color derived from the original photograph, unless the user supplies an exact color.
- Space: visible background around the poster and between panels.
- Resolution: moderate social-media resolution by default.
- Text: none by default. Do not invent `BEFORE`, `AFTER`, dates, credits, locations, or captions.

## Social Output Card

Build a JSON card conforming to [social-output-card.schema.json](social-output-card.schema.json). Defaults:

- `canvas_ratio`: `4:5`;
- `canvas_width`: `1080`;
- `background_strategy`: `source_warm`;
- `background_color`: `null`;
- `original_position`: `top`;
- `generated_position`: `bottom`;
- `fit`: `contain`;
- `panel_width_percent`: `84`;
- `outer_margin_percent`: `6`;
- `inter_panel_gap_percent`: `4`.

Use `9:16` for Stories/Reels or `1:1` only when the destination or user asks. Keep `contain` so neither image is silently cropped.

## Composition workflow

Run from the skill directory:

```bash
python3 scripts/compose_comparison_poster.py \
  --original /path/to/original.jpg \
  --generated /path/to/generated.png \
  --card /path/to/social-output-card.json \
  --output /path/to/comparison-poster.png
```

The compositor samples the original for a warm seed, lightens and desaturates it into a quiet paper-like background, then independently contains both panels in equal vertical slots. Use `background_strategy=custom` with an exact `#RRGGBB` value when the user specifies a color.

Do not pass the poster through an image-generation model. That could alter the original panel, the accepted artwork, or the spacing contract.

## Delivery QA

- [ ] The original is above and the generated artwork is below.
- [ ] The original panel has not been retouched, cropped, regenerated, or color-shifted.
- [ ] The generated panel matches the accepted artwork.
- [ ] Both panels retain their full aspect ratios under `contain`.
- [ ] Warm background is visible on all four sides and between panels.
- [ ] The background supports the source palette without competing with either panel.
- [ ] No label, caption, watermark, frame shadow, tape, or decorative prop was invented.
- [ ] The poster remains legible at social-feed size.

If poster QA fails, recomposite only. Do not regenerate the artwork.
