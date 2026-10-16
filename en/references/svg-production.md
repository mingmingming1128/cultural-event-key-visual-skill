# Hybrid editable SVG production

Read only after one exact ImageGen high-fidelity PNG has explicit user approval, and again before final delivery.

## Assembly contract

The final SVG is a layered production file built from three sources:

1. a cleaned ImageGen PNG containing only the approved visual imagery;
2. editable SVG text replacing every rendered text glyph;
3. original uploaded files replacing logos, QR codes, seals, sponsor marks, and similar assets.

Do not redraw the entire approved composition with vector paths. Do not embed the uncleaned approved PNG. The full-canvas raster is allowed only after text and replaceable original assets have been removed and their former regions have been cleanly restored.

## 1. Classify the approved PNG

Before editing, make a region inventory:

- `visual-base content`: designed imagery, photography, illustration, atmosphere, texture, lighting, color fields, and decorative visual effects that should remain in the PNG;
- `editable text`: title, subtitle, date, time, venue, organizer, body copy, labels, CTA, and any other communicative wording;
- `replaceable original asset`: supplied logos, QR codes, seals, sponsor or partner marks, certification marks, signatures, badges, and other files whose original pixels or vectors must be preserved.

When classification is ambiguous, prefer editability for language and fidelity to the original upload for identity or machine-readable marks. Do not remove a hero photograph or illustration merely because it came from an upload when it functions as part of the designed visual imagery.

## 2. Produce the cleaned visual base

Edit the exact approved ImageGen PNG and save the derivative as `svg-reconstruction/imagegen-visual-base.png`.

- Remove all visible text, including decorative lettering, generated pseudo-text, dates, credits, tiny labels, and text shadows or glow remnants.
- Remove every replaceable original asset, including generated or distorted imitations of logos and QR codes.
- Inpaint each removed region using the surrounding visual language so the base looks intentional without overlays.
- Preserve canvas size, crop, composition, visual imagery, palette, texture, lighting, and negative space.
- Do not introduce new objects, symbols, words, logos, or layout changes during cleanup.
- Compare the cleaned base directly against the approved PNG. If a retained visual element changed, correct the cleanup before assembling SVG.

The cleaned PNG is a production derivative. It does not replace the approved reference and must not overwrite it.

## 3. Assemble SVG layers

Use these named groups in back-to-front order:

- `visual-base`: contains exactly one full-canvas `image` with `id="imagegen-visual-base"` and `data-source-kind="imagegen-visual-base"`;
- `vector-adjustments`: optional native SVG geometry used only for production adjustments such as text backplates, clipping, or simple separators;
- `original-assets`: contains the original uploaded logo, QR code, seal, sponsor mark, or similar files;
- `editable-text`: contains all communicative copy as SVG `text` and `tspan` elements.

The root `svg` must include numeric `width`, `height`, and a four-number `viewBox` matching the cleaned PNG aspect ratio.

### Visual-base image

- Use the cleaned PNG, never the uncleaned approved PNG.
- Set `x="0"`, `y="0"`, and dimensions that cover the full viewBox without an unintended crop.
- Give the image the exact ID and source-kind marker above.
- Use an embedded PNG data URI for a self-contained SVG or a relative path delivered beside the SVG.
- Do not vector-trace the base.

### Editable text

- Use exact approved copy in `text` and `tspan` elements.
- Keep titles, subtitles, dates, times, venues, organizers, body copy, credits, labels, and CTAs editable.
- Do not convert ordinary copy only to paths. If an outlined display duplicate is necessary, retain a correctly positioned editable text source layer.
- Match the approved hierarchy, alignment, line breaks, tracking, leading, color, and placement while improving factual accuracy and legibility.
- Ensure no text or text-like ghost remains in the cleaned PNG below the SVG copy.

### Original uploaded assets

- Embed each original file as its own `image` element with a stable ID such as `asset-ASSET-001` and `data-source-kind="original-upload"`.
- Use the original uploaded file from `source/supplied-assets/`; do not crop a replacement out of the ImageGen PNG and do not synthesize an imitation.
- Preserve aspect ratio and required clear space. Do not distort, recolor, redraw, or apply generative cleanup unless the user's notes explicitly permit it.
- For QR codes, preserve the complete code and quiet zone, avoid filters or interpolation effects, and verify scanability from the rendered final output.
- If no original file is available, do not silently keep the ImageGen imitation. Omit it or use an explicit placeholder and report the missing asset.

## Compatibility target

Produce standards-based SVG that imports cleanly into common vector editors. Use ordinary groups, images, text, shapes, gradients, and clipping paths.

Avoid:

- `foreignObject`;
- scripts and event handlers;
- animation;
- browser-only layout;
- external CSS;
- remote image URLs;
- unnecessary filters, masks, and blend modes with poor editor support.

Prefer embedded data URIs for a self-contained SVG. If image files remain external, use relative paths and deliver them beside the SVG. Record font family, weight, source, license or availability, and fallback in `font-manifest.md`; do not redistribute fonts without authorization.

## Fidelity comparison

Render the final SVG at the approved PNG dimensions and compare:

- retained visual imagery, silhouette, palette, texture, and spacing;
- absence of text, logo, QR-code, or badge remnants in the visual base;
- exact copy, hierarchy, line breaks, and alignment of editable text;
- geometry, color, aspect ratio, clear space, and placement of original assets;
- QR-code scanability where applicable;
- full-size and thumbnail reading order.

Document intentional differences. Fix cleanup defects in the visual-base PNG; fix copy and supplied-asset defects in the responsible SVG layer. Return to concept generation only when the user explicitly reopens the approved design.

## Final checks

1. Parse as XML and confirm root size and `viewBox`.
2. Confirm the `visual-base`, `original-assets`, and `editable-text` groups exist.
3. Confirm exactly one `imagegen-visual-base` image exists, points to PNG data, and carries the correct `data-source-kind`.
4. Confirm the visual-base PNG contains no rendered text or replaceable supplied assets.
5. Confirm all communicative copy exists as editable `text` or `tspan`.
6. Confirm every embedded logo, QR code, seal, sponsor mark, or similar item comes from an original upload and carries `data-source-kind="original-upload"`.
7. Resolve all image references and reject remote URLs.
8. Render and inspect at full size and thumbnail size; scan-test QR codes.
9. Import into an independent editor when available and verify text editing, group separation, image replacement, and font fallback.
