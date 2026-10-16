# Skill testing protocol

Use the same task and evidence set when comparing revisions.

## Accuracy

Run the skill more than once and check:

- form creation and brief parsing;
- factual copy;
- required and prohibited assets;
- language equivalence;
- layout relationships and readability;
- ImageGen prompt completeness and version preservation;
- correct routing of user feedback into ImageGen edits before approval;
- explicit approval of one exact ImageGen version before SVG work;
- visual fidelity between the approved ImageGen image and assembled SVG;
- complete removal of rendered text and replaceable assets from the cleaned ImageGen PNG;
- use of original uploaded logos, QR codes, seals, and similar assets in separate SVG layers;
- SVG dimensions, required groups, editable text, source-kind markers, and compatibility;
- enforcement of the single ImageGen approval gate.

## Stability

Express the same task as a formal brief, conversational request, short command, structured JSON, and another supported language. Distinguish wording changes from real requirement changes before comparing behavior.

## Quality and cost

Compare:

- completion rate;
- output quality;
- preservation of core capabilities;
- unnecessary questions and repeated work;
- execution time and token cost;
- number of ImageGen generations and avoidable broad regenerations;
- ImageGen cleanup effort, SVG assembly effort, and failures to preserve original assets.

Remove rules that add cost without observable benefit.

## Usability

Give the skill and test materials to someone who did not write it. Observe whether they can:

- complete the form without oral guidance;
- supply images;
- understand the ImageGen review and revision loop;
- identify the exact approved ImageGen version;
- request a revision;
- receive and edit the final SVG;
- repeat the workflow for another cultural event.

Record concrete obstacles, make the narrowest correction, and rerun the same test.
