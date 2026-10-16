# Cultural Event Key Visual Skill

A bilingual Codex Skill for producing cultural-event key visuals from an interactive intake form through ImageGen review and editable SVG delivery.

## Languages

- [`zh-CN/`](./zh-CN/) — 中文版
- [`en/`](./en/) — English version

Each language directory is a complete, independently usable Skill package. Copy the directory for the language you need into your Codex skills directory, or use it directly from a compatible workspace.

## Workflow

1. Collect optional requirements and uploaded visual assets through an interactive form.
2. Complete missing details from the available context.
3. Generate a high-fidelity key visual with ImageGen.
4. Revise the design until the user approves it.
5. Produce an editable SVG: retain the approved visual artwork as the base image, replace text with SVG text, and embed original assets such as logos separately.

## Repository layout

```text
.
├── zh-CN/   # Complete Chinese Skill
└── en/      # Complete English Skill
```

