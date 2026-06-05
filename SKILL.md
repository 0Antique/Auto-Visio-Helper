---
name: auto-visio-helper
description: Help Codex plan, generate, reproduce, and refine editable Microsoft Visio scientific diagrams. Use when users ask Codex to operate local Visio, create VSDX research figures, redraw uploaded paper screenshots or sketches in Visio, convert natural-language method descriptions into scientific diagrams, export preview PNG/PDF/SVG, or build editable model architecture, workflow, system architecture, experiment, pseudo-code, sequence, or module interaction diagrams.
---

# Auto Visio Helper

Use this skill to turn vague research-figure requests into editable Visio diagrams. Always plan the diagram as a verifiable drawing spec before driving local Visio.

## Core Workflow

1. Classify the task:
   - `description_to_diagram`: user describes a method, model, system, or experiment.
   - `image_reproduction`: user uploads a paper figure, sketch, PPT screenshot, or reference image.
   - `paper_redraw`: user wants a cleaner publication-ready version, not a strict copy.
   - `visio_refine`: user wants to modify an existing VSDX or exported preview.

2. Gather only blocking requirements:
   - Language: Chinese, English, or bilingual.
   - Target use: paper, thesis, defense slides, project report, patent, or internal note.
   - Layout width: single-column, double-column, A4, slide, or custom size.
   - Style target: IEEE, Nature-like, clean engineering, Chinese thesis, or strict reference matching.
   - Export target: always propose preview exports (`.png`, optionally `.pdf` / `.svg`) before finalizing `.vsdx`.

3. Produce a short design brief and a structured drawing spec first. Do not start Visio automation until the user has confirmed the spec or clearly asked to proceed without confirmation.

4. Render the confirmed drawing spec with `scripts/render_visio.py` when Microsoft Visio is available on Windows. Keep all diagram elements editable: use Visio shapes, connectors, text, layers, names, and groups instead of flattening the diagram into one pasted image.

5. Export preview files, inspect them, compare against the request or source image, then iterate on the drawing spec if needed.

## Required Drawing Spec

Use JSON as the intermediate representation. Read [references/drawing_spec.md](references/drawing_spec.md) before writing a complex spec.

Minimum shape:

```json
{
  "page": {"width_mm": 297, "height_mm": 210, "unit": "mm"},
  "style": {"font": "Arial", "font_size_pt": 9, "theme": "paper_clean"},
  "nodes": [],
  "edges": [],
  "groups": [],
  "annotations": [],
  "exports": {"png": true, "pdf": false, "svg": false}
}
```

Use top-left coordinates in millimeters. Name every node and connector with stable IDs so the VSDX remains editable and reviewable.

## Reference Files

Load only the file needed for the current task:

- [references/diagram_types.md](references/diagram_types.md): choose diagram type and layout pattern.
- [references/drawing_spec.md](references/drawing_spec.md): JSON schema and examples.
- [references/style_guide.md](references/style_guide.md): publication-oriented fonts, colors, spacing, and line rules.
- [references/visio_automation.md](references/visio_automation.md): local Visio COM automation notes and troubleshooting.

If a Visio template file is present, such as `references/绘图模版.vsdx`, treat it as a reusable local template. Do not load binary templates into context; pass their path to scripts or copy them as needed.

## Image Reproduction Rules

For uploaded reference images:

1. Decide whether the user wants structure reproduction, visual reproduction, or publication-grade redraw.
2. Extract visible text, modules, hierarchy, arrows, color families, and layout proportions.
3. Rebuild the image as editable Visio primitives. Do not paste the image as the final diagram.
4. Export a preview and compare these points: missing nodes, wrong arrow direction, text mismatch, layout drift, inconsistent spacing, and style mismatch.

## Quality Gate

Before final delivery, verify:

- Text does not overlap shapes or connectors.
- Arrow direction matches the intended data/control flow.
- Same-level modules share consistent size, alignment, and spacing.
- Font size is readable at the target paper or slide size.
- Color count is controlled and black-white printing remains understandable when requested.
- Line width, arrowheads, corner radius, and padding are consistent.
- `.vsdx` keeps editable shapes, connectors, groups, layers, and named text boxes.
- Preview exports match the confirmed spec closely enough for user review.

## Script Usage

Validate a spec without opening Visio:

```powershell
python scripts/render_visio.py spec.json --dry-run
```

Render with local Visio:

```powershell
python scripts/render_visio.py spec.json --output output\diagram.vsdx --export-png output\diagram.png
```

Use `--template references\绘图模版.vsdx` when a local Visio template should define page theme, stencils, or base styles.
