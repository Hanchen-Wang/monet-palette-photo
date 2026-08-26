# Full Impression

Use only when the user explicitly wants the complete photograph repainted.

## Source contract

- Source role: factual and compositional anchor.
- Source pixels in final: none.
- Preserve: primary subject identity, pose, relative positions, perspective, horizon, light direction, and scene-specific objects.
- Transform: every visible region through surface-responsive impressionist color and brush construction.
- Do not: introduce new scenery or replace the source with a generic garden, pond, bridge, sunset, or pastoral scene.

## Analysis focus

Build the normal Impressionability Map, but use it to vary intensity rather than decide whether a zone is painted. High-scoring zones receive stronger broken color, edge loss, and brush visibility; stable semantic anchors remain more defined.

## Composition and strength

- Default strength: M3.
- Default presentation profile: `immersive`.
- Retain the source composition unless the user requests a reframe.
- Keep faces and hands relatively stable at M1–M3; only M4 may dissolve them, and only when the user explicitly accepts reduced identity fidelity.
- Use chromatic darks and source-responsive warm/cool variation throughout, not a uniform pastel wash.

## Hard avoids

- one identical oil texture over the entire image;
- arbitrary impasto unrelated to surface or depth;
- black or gray shadows with no color variation;
- loss of source-specific architecture, anatomy, or perspective;
- fake Monet motifs not present in the source.
