# ImageGen high-fidelity production

Read before the first ImageGen generation and every ImageGen revision.

## First generation

Generate the first visible design directly at high fidelity. Build one structured prompt from the brief synthesis with:

- event purpose, audience, channel, and aspect ratio;
- one clear visual idea and cultural basis;
- composition, hierarchy, reading path, and negative space;
- palette, material, lighting, texture, and image treatment;
- typography behavior and reserved zones for exact copy;
- supplied-image roles and preservation constraints;
- prohibited motifs, unsafe cultural uses, and unsupported claims.

Use supplied images only within their recorded role and rights. When an image is a reference rather than required content, extract visual behavior instead of copying protected details.

ImageGen is a visual-composition source, not a factual authority. Do not trust generated letterforms, dates, logos, QR codes, or legal text. After image approval, remove all rendered wording and replaceable assets from a cleanup copy of the PNG; exact copy becomes editable SVG text, while logos, QR codes, seals, and similar items come from the original uploads.

## Versioning and presentation

Save generations as immutable numbered files such as `imagegen-v01.png`, `imagegen-v02.png`, and so on. For each version record:

- complete generation or edit prompt;
- source image references;
- intended changes from the previous version;
- accepted regions to preserve;
- inferred decisions and unresolved factual limitations.

Present the actual image with its version number, concise rationale, and known issues. Ask the user either to approve that exact version or describe changes. Do not infer approval from silence or a generic request to continue.

## Revision loop

Convert feedback into an edit specification with:

- object or region to change;
- observed problem;
- intended result;
- elements that must remain unchanged;
- acceptance check.

Use the latest intended image as the edit reference. Prefer a local edit when the user requests a local change. Regenerate broadly only when composition, concept, or overall style changes. Never overwrite an earlier version.

If user feedback conflicts with confirmed facts, rights, or cultural restrictions, explain the conflict and preserve the constraint. Otherwise continue the ImageGen revision loop until explicit approval.

## Approval record

Approval must identify one exact version. Record the filename, version number, user wording, and timestamp before SVG assembly. Any later concept or design change in ImageGen invalidates the prior approval and requires approval of the new version.

## Post-approval cleanup edit

After approval, ImageGen may be used once more as a production cleanup tool rather than a concept generator. Edit the exact approved PNG to remove text and replaceable original assets, inpaint the vacated regions, and preserve every visual element. Save this as `imagegen-visual-base.png` without overwriting the approved reference. A cleanup that changes composition, imagery, palette, texture, or spacing is not acceptable; correct it or return to the approved source. Follow [svg-production.md](svg-production.md) for classification, assembly, and verification.
