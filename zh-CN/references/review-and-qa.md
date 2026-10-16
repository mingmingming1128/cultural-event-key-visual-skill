# Review gate and quality assurance

## ImageGen high-fidelity review package

Provide:

- the numbered high-fidelity ImageGen image;
- concept and cultural basis;
- information hierarchy and reading path;
- supplied/generated asset use;
- changes from the previous ImageGen version, when applicable;
- known factual, rights, typography, or rendering limitations.

Ask the user to approve that exact version or request changes. Stop. Do not interpret silence, approval of an earlier version, or a vague continuation as approval. Continue ImageGen revisions until one exact version is explicitly approved.

## Hybrid SVG assembly review package

After approval, provide:

- the approved ImageGen reference;
- cleaned `imagegen-visual-base.png`;
- assembled SVG and matching rendered preview;
- visual comparison notes covering composition, color, imagery, typography, and spacing;
- confirmation that the cleaned PNG contains no text, logo, QR-code, seal, or partner-mark remnants;
- mapping from each original uploaded asset to its SVG image layer;
- factual copy check;
- editability and compatibility check;
- unresolved fidelity differences.

SVG assembly follows the approved design; it is not a second concept stage. Fix base-cleanup defects in the cleanup PNG and overlay defects in SVG. Return to concept generation only when the user explicitly reopens the visual design, in which case the new ImageGen result needs a new approval.

## Hard failure gates

Fail the candidate if any condition applies:

- SVG assembly began without one recorded, explicitly approved ImageGen version;
- the approved ImageGen version cannot be identified from the workflow state and revision log;
- event title, date, time, venue, organizer, or mandatory CTA is wrong;
- required copy or asset is missing;
- language variants disagree;
- text is unreadable, clipped, or garbled;
- a protected or sensitive cultural element is used without adequate basis;
- dimensions, ratio, or output count are wrong;
- SVG cannot parse, lacks a valid `viewBox`, uses forbidden active content, lacks exactly one correctly marked cleaned ImageGen PNG base, or embeds the uncleaned approved PNG;
- the cleaned visual base still contains rendered text or replaceable assets;
- a logo, QR code, seal, sponsor mark, or similar item uses an ImageGen imitation when an original upload is available;
- an original asset is distorted, incorrectly cropped, or unusable; a QR code fails a scan test;
- mandatory event text is not editable without an approved reason.
- assembled SVG materially departs from the approved ImageGen composition without recorded user approval.

## Weighted review

| Dimension | Weight |
|---|---:|
| Information accuracy | 25 |
| Hierarchy and readability | 20 |
| Cultural relevance and appropriateness | 20 |
| Visual finish | 15 |
| Audience and communication fit | 10 |
| Hybrid SVG fidelity and editability | 10 |

Pass at 80 or above only when all hard gates pass.

## Actionable feedback

Translate feedback into:

- object;
- observed problem;
- intended result;
- local adjustment or regeneration;
- acceptance check.

Before ImageGen approval, revise the smallest responsible image region and preserve every prior generation. After approval, revise the cleaned PNG only for residual visual-base content and revise SVG for text or original-asset overlays. Never overwrite the approved ImageGen reference.
