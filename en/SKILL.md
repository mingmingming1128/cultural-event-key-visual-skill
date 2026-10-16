---
name: cultural-event-key-visual-en
description: Create cultural-event key visuals by collecting an optional brief, generating and revising a high-fidelity design with ImageGen, obtaining explicit user approval, and assembling a hybrid editable SVG from a cleaned ImageGen PNG, editable text, and original supplied assets. Use for exhibitions, festivals, performances, lectures, and other cultural-event promotion. Do not use for ordinary product advertising, logo-only work, or document layout.
---

# Cultural Event Key Visual

Produce a traceable cultural-event visual through an ImageGen-first workflow. Keep confirmed facts separate from inference, use ImageGen for the complete high-fidelity design and revision loop, then convert only the explicitly approved version into a hybrid editable SVG.

## Non-negotiable contract

1. Start by creating and presenting the fillable intake form from `assets/intake-form-template.html`, even when the user already supplied a detailed brief. Prefill known facts when practical; the user verifies or edits them.
2. Treat every intake-form field as optional. Summarize the returned brief, but never block concept generation because a field is blank. Infer necessary design decisions from the available context and label them; resolve only explicit contradictions or rights/safety issues before using the affected material.
3. Use ImageGen to produce the first visual output directly at high fidelity. Do not insert a low-fidelity SVG stage.
4. Revise the high-fidelity image with ImageGen in response to user feedback, preserving each numbered version. Begin hybrid SVG assembly only after the user explicitly approves one exact ImageGen version.
5. Silence, approval of an earlier version, or an ambiguous "continue" does not approve the current ImageGen version.
6. Build the final SVG from a cleaned copy of the approved ImageGen PNG. The cleaned PNG retains only the designed visual imagery; remove all rendered text and replaceable supplied assets such as logos, QR codes, seals, and partner marks. Use the cleaned PNG as the visual-base image, recreate all copy as editable SVG `text`/`tspan`, and embed each replaceable item from its original uploaded file.

Use `scripts/create_project.py` to initialize the project form and folders. It copies `serve-form.py` into the project. Start that local service and present its `http://127.0.0.1:<port>/intake-form.html` URL; the form then saves directly to its own project workspace without a folder picker. Use `scripts/validate_brief.py` on the returned JSON and `scripts/validate_svg.py` before final delivery.

## Workflow

### 1. Intake

- Create a project workspace and form, start the copied `serve-form.py`, and open the reported local URL. Do not open `intake-form.html` through `file://` or a generic static server because direct workspace saving requires the project service.
- Let the user fill the form and supply images through its dedicated image-upload step, chat attachments, or `source/supplied-assets/`. The form upload is the default: each image retains a stable ID, preview, use mode, purpose selection, and optional edit restrictions.
- Validate a partial `brief.json` with `scripts/validate_brief.py --stage intake`; after review, use `--stage imagegen` before high-fidelity generation. Blank fields produce non-blocking guidance, not validation failure. A downloaded draft is not approval. The legacy `--stage concept` name remains an alias for older projects.
- Summarize confirmed facts, blank fields, inferred or generated defaults, supplied assets, forbidden elements, and language versions. Continue to ImageGen high fidelity even when every form field is blank.
- Read [intake-and-content.md](references/intake-and-content.md) for field rules, source status, and image intake.

### 2. Direction and ImageGen prompt

- Separate cultural facts, contemporary reinterpretations, commercial references, and unknown material.
- Extract visual genes such as composition, rhythm, palette, material, spatial logic, and motion. Do not reduce culture to decorative symbols.
- Choose one strong direction by default. If the user explicitly requests exploration, generate clearly separated high-fidelity alternatives rather than low-fidelity sketches.
- Convert the direction into a structured ImageGen prompt covering composition, hierarchy, palette, material, imagery, typography behavior, cultural constraints, supplied-asset roles, output ratio, and prohibited elements.
- Read [cultural-direction.md](references/cultural-direction.md) when cultural sources, references, sensitive material, or multiple concepts are involved.
- Read [imagegen-production.md](references/imagegen-production.md) before generating or revising the high-fidelity image.

### 3. ImageGen high-fidelity generation and revision

- Generate a complete high-fidelity key visual with ImageGen in one step from the approved brief synthesis and prompt.
- Save each result as an immutable numbered version and record its prompt, supplied references, inferred decisions, and known factual or rendering limitations.
- Present the high-fidelity image with a concise design rationale and factual-copy caveats. Ask the user to approve this exact version or provide changes.
- For revisions, translate feedback into explicit deltas and edit the latest intended version with ImageGen. Preserve accepted regions when the feedback is local.
- Repeat the revision loop until the user explicitly approves one exact version. Do not write the final SVG during this loop.

### 4. Approval gate and hybrid SVG assembly

- Record the approved ImageGen filename/version, approval wording, and timestamp in `workflow-state.json` and `revision-log.md`.
- Read [svg-production.md](references/svg-production.md), then inventory the approved PNG into three classes: `visual-base content`, `editable text`, and `replaceable original asset`.
- Create `svg-reconstruction/imagegen-visual-base.png` by editing the approved PNG: remove every text glyph and every replaceable image asset, then inpaint those regions from the surrounding design. Preserve all other composition, imagery, color, texture, lighting, and spacing. This cleanup is a production derivative, not a newly approved concept.
- Use the cleaned PNG as one full-canvas SVG `image` named `imagegen-visual-base` with `data-source-kind="imagegen-visual-base"`.
- Recreate every title, subtitle, date, time, venue, organizer, body block, label, and CTA as editable SVG `text`/`tspan`. The cleaned PNG must contain no duplicate or ghosted lettering beneath it.
- Remove logos, QR codes, seals, sponsor marks, certification marks, and similar replaceable assets from the PNG, then embed the corresponding original files from `source/supplied-assets/` as separate SVG `image` elements with `data-source-kind="original-upload"`. Never use an ImageGen-rendered imitation when an original file exists.
- Keep `visual-base`, `original-assets`, and `editable-text` as separate named groups. Optional native SVG shapes may be used for adjustment layers, but do not vector-trace the ImageGen visual base.
- Render the assembled SVG and compare it with the approved ImageGen version at full size and thumbnail size. Check that cleanup did not damage visual elements, text is editable and exact, and original assets retain correct geometry and scanability.

### 5. Final SVG and delivery

- Clean names and groups, resolve the cleaned PNG and original uploaded assets, preserve editable text, and add a font manifest.
- Run the SVG validator and render the validated file again for visual inspection.
- Apply the hard gates and scoring in [review-and-qa.md](references/review-and-qa.md).
- Deliver the approved ImageGen reference, `imagegen-visual-base.png`, `final-editable.svg`, a rendered SVG preview, the original embedded assets or their resolvable relative files, `font-manifest.md`, `qa-report.md`, and `revision-log.md`. For multilingual or multi-size work, deliver a separately adapted SVG for each variant.

## Revision routing

Change the smallest responsible layer:

- mistranslation -> language variant;
- cultural misuse -> source classification or visual genes;
- feedback before ImageGen approval -> ImageGen revision prompt;
- residual text or generated asset in the visual base -> ImageGen cleanup edit;
- text, logo, QR code, or placement mismatch after approval -> the responsible SVG overlay layer;
- incorrect facts -> editable SVG text and content master, without silently changing the approved visual direction;
- rejected approved direction -> explicitly reopen ImageGen generation and require a new approval.

Never overwrite an approved draft while exploring a revision.

## Testing the skill

For skill evaluation or refinement, read [testing-protocol.md](references/testing-protocol.md). Test accuracy, stability, quality/cost, and independent usability with saved before/after evidence.
