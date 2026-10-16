# Intake and content control

Read this reference during intake, when supplied images are present, or when facts conflict.

## Form contract

Always provide the generated `intake-form.html`. Every visible field is optional. Prefill only facts visible in the user's message or attachments; do not convert guesses into prefilled facts. A completely blank form may still be exported and must not block ImageGen generation. Run `validate_brief.py --stage intake` to check its structure; run `validate_brief.py --stage imagegen` after human review and before high-fidelity generation. Missing optional values may produce warnings, but warnings do not invalidate the brief. `--stage concept` is retained only as a compatibility alias for older projects.

The form exports:

- activity classification, formal name, and theme;
- target audience, communication goal, and optional combined participation information;
- visual style, color preferences, and composition preferences, each accepting free text and repeatable preset suggestions that append into the same text field;
- individually numbered text blocks with a first-level purpose group, a dependent second-level material type, content, and a processing requirement (`editable`, `full-verbatim`, or `generation-prompt`);
- individually numbered images with exactly one use mode (`required` or `visual-reference`), a purpose selection, and optional edit restrictions;
- overall language requirements, including a named other language when selected;
- individually numbered deliverables with dropdown selections for type, channel, and dimensions or aspect ratio.

The form includes a dedicated image-upload step with click-to-select, drag-and-drop, per-image previews, and per-image metadata. It offers two actions: save a browser draft, or save all project materials directly to the current project workspace. `create_project.py` copies `serve-form.py` into each project; open the form through that local service. The save action writes `brief.json` to the project root and copies selected images into `source/supplied-assets/` without asking the user to choose a folder. A generic static server or `file://` cannot provide this filesystem write path.

### Deliverable selections

- Type options cover key visuals, posters, social-media images and covers, banners, invitations, signage, digital screens, and an `other` fallback.
- Channel options cover print, venue display, WeChat Official Accounts, WeChat Moments, Xiaohongshu, Weibo, Douyin or short-video platforms, websites, digital displays, and an `other` fallback.
- Specification options cover common square, portrait, vertical-video, landscape, poster, and A-series print formats, plus an `other` fallback.
- Each deliverable row describes one type/channel/specification combination. Add another row for a second channel or size. Fields remain optional; when omitted or set to `other`, infer a suitable value from the rest of the brief and label that inference.

The form's review summary lists what was provided and what still needs checking. It does not automatically approve the brief. Before ImageGen generation, show the demand analysis to the task initiator; if this is a classroom simulation without an external client, the student using the skill records a reasoned review or asks a designated group reviewer. A request for the initiator's own approval cannot be replaced by self-review. The form exports confirmation as pending; after review, record the reviewer and set `confirmation.status=confirmed` in the brief before running the ImageGen-stage validator.

Uploaded file objects cannot survive browser-draft reloads. The form restores text and image notes, then asks the user to select the files again. Exported JSON alone does not include file bytes.

### Text material categories

Choose a broad first-level purpose, then the narrowest available second-level type:

| First-level purpose | Second-level material types |
|---|---|
| `promotional-copy` | `headline` title/theme/slogan; `event-description` event introduction or core promotional copy |
| `event-facts` | `event-time` date/time; `event-location` venue/platform; `organizer` formal organizer; `program` agenda/session information; `participation` registration/ticketing/admission |
| `cultural-content` | `curatorial` curatorial/project interpretation; `background` cultural or historical context; `person-work` person/group/collection/work introduction |
| `credits-compliance` | `credit` partner/sponsor/attribution; `legal` copyright/legal/safety/risk notice |
| `language-other` | `translation` approved translation or foreign-language copy; `other` material outside the maintained taxonomy |

In schema 2.4, save the first level as `purpose_group` and the second level as `category`. The category must belong to the selected purpose group. When loading an older brief that contains only `category`, derive `purpose_group` from this table.

Do not infer missing factual copy from its category. A category organizes supplied content; it does not change the source-status rules below.

### Text processing requirements

- `editable`: the supplied text may be condensed, reorganized, or rewritten without changing verified facts;
- `full-verbatim`: preserve the complete block exactly as supplied;
- `generation-prompt`: treat the block as instructions or source constraints for generating new copy, not as copy to place verbatim in the artwork.

Any copy produced from `generation-prompt` starts with `GENERATED` source status. Present it for human review before promoting it to approved copy, and never invent dates, venues, organizers, ticketing, partner names, legal claims, or other factual event information from the prompt.

## Source status

Use these statuses in the content master:

- `VERIFIED`: explicitly supplied by the user or an authoritative source.
- `INFERRED`: reasonable design inference, never a factual claim.
- `GENERATED`: AI-created copy or visual content.
- `MISSING`: not supplied.
- `CONFLICT`: sources disagree.
- `DO_NOT_EDIT`: preserve verbatim.

Dates, venue, organizer, ticketing, event title, partners, and legal copy may not be inferred.

## Auto-completion and blockers

Blank fields never block ImageGen high-fidelity generation. Derive necessary working decisions from the strongest available evidence in this order: confirmed text, supplied images and references, surrounding conversation, then conservative design defaults.

- Mark derived preferences, audience assumptions, format choices, and visual direction as `INFERRED`.
- Mark newly written non-factual copy as `GENERATED` and present it for review.
- Propose reasonable canvas dimensions, language, hierarchy, palette, and composition when omitted.
- Do not invent event title, date, venue, organizer, ticketing terms, partner names, legal claims, or image rights. Omit them or use explicit draft placeholders until confirmed.
- Do not use an image publicly while its rights or cultural-use restrictions remain uncertain; ImageGen may use a neutral labeled placeholder or omit the affected material.

Only explicit contradictions, unsafe cultural use, or unusable/corrupt supplied files block use of the affected material. They do not prevent generation of the rest of the concept.

## Content master

Create one source of truth with, at minimum:

| Field | Source text | Approved variant | Status | Required | Editable | Source |
|---|---|---|---|---|---|---|

Every language and size variant must trace back to this table. When it changes, recheck every downstream SVG.

## Supplied image intake

For each image, record:

- stable asset ID;
- original filename;
- one use mode: required in the final work, or visual reference only;
- one purpose selection: `hero`, `background`, `color-reference`, `layout-reference`, `style-reference`, `composition-reference`, `motif-reference`, or `other`;
- notes, including requested crop, color treatment, preservation, or other usage constraints;
- cultural meaning and edit restrictions when known;
- dimensions and file type;
- risk level.

Never silently replace a required user image. Preserve originals and perform edits non-destructively.
