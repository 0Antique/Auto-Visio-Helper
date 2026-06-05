# Auto-Visio-Helper

Auto-Visio-Helper is a Codex skill for planning, generating, reproducing, and refining editable Microsoft Visio scientific diagrams. It helps Codex convert natural-language research descriptions or reference images into a structured drawing spec, then render the confirmed spec into editable `.vsdx` files with optional preview exports.

## Repository Description

Codex skill for creating editable Microsoft Visio research diagrams from text descriptions or reference images, with JSON drawing specs, local Visio automation, and preview export support.

## What It Does

- Turns vague research-figure requests into a reviewable JSON drawing spec.
- Creates editable Visio diagrams instead of flattened pasted images.
- Supports model architecture diagrams, method workflows, system architectures, experiment flows, concept figures, pseudo-code diagrams, sequence diagrams, and module interaction diagrams.
- Supports image reproduction from paper screenshots, hand-drawn sketches, and PPT screenshots.
- Encourages a confirm-before-render workflow: plan first, preview second, finalize `.vsdx` after review.
- Provides a Python script for rendering JSON specs through local Microsoft Visio COM automation.

## Workflow

1. Understand the user request or uploaded reference image.
2. Classify the task as description-to-diagram, image reproduction, paper redraw, or Visio refinement.
3. Generate a concise design brief and structured drawing spec.
4. Ask the user to confirm the spec or requested preview export formats.
5. Render the confirmed spec with local Visio.
6. Export previews such as `.png`, `.pdf`, or `.svg`.
7. Inspect and iterate until the diagram is publication-ready.

## Directory Structure

```text
Auto-Visio-helper/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── diagram_types.md
│   ├── drawing_spec.md
│   ├── style_guide.md
│   ├── visio_automation.md
│   └── 绘图模版.vsdx
├── scripts/
│   └── render_visio.py
└── 需求.md
```

## Installation

Copy or clone this folder into your Codex skills directory:

```powershell
git clone <your-repo-url> $env:USERPROFILE\.codex\skills\auto-visio-helper
```

Then restart Codex or reload skills if your environment requires it.

## Requirements

For spec planning and dry-run validation:

- Python 3.10+

For actual Visio rendering:

- Windows
- Microsoft Visio desktop installed and licensed
- Python package `pywin32`

Install `pywin32`:

```powershell
python -m pip install pywin32
```

## Script Usage

Validate a drawing spec without opening Visio:

```powershell
python scripts\render_visio.py spec.json --dry-run
```

Render an editable Visio file:

```powershell
python scripts\render_visio.py spec.json --output output\diagram.vsdx --export-png output\diagram.png
```

Render with the included Visio template:

```powershell
python scripts\render_visio.py spec.json --template references\绘图模版.vsdx --output output\diagram.vsdx --export-png output\diagram.png
```

## Drawing Spec Example

```json
{
  "page": {"width_mm": 180, "height_mm": 90, "unit": "mm", "title": "YOLO flow"},
  "style": {"font": "Arial", "font_size_pt": 9, "theme": "paper_clean"},
  "nodes": [
    {"id": "input", "label": "Input image", "shape": "parallelogram", "x_mm": 10, "y_mm": 32, "width_mm": 34, "height_mm": 18},
    {"id": "backbone", "label": "Backbone", "shape": "rounded_rectangle", "x_mm": 58, "y_mm": 28, "width_mm": 38, "height_mm": 26},
    {"id": "head", "label": "Detection head", "shape": "rounded_rectangle", "x_mm": 112, "y_mm": 28, "width_mm": 46, "height_mm": 26}
  ],
  "edges": [
    {"id": "e1", "from": "input", "to": "backbone", "arrow": "end"},
    {"id": "e2", "from": "backbone", "to": "head", "arrow": "end"}
  ],
  "groups": [],
  "annotations": [],
  "exports": {"png": true, "pdf": false, "svg": false}
}
```

## Skill Invocation Example

```text
Use $auto-visio-helper to create an editable Visio diagram for my YOLO11 pest detection method. Include dataset preprocessing, backbone, feature fusion, detection head, loss, and output prediction.
```

## Notes

- The final diagram should use editable Visio shapes, connectors, text boxes, layers, and names.
- Do not use a pasted bitmap as the final result for image reproduction tasks.
- Use `references/drawing_spec.md` as the contract between diagram reasoning and Visio automation.
- Use `references/style_guide.md` to keep paper figures readable and consistent.
