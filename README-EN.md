# Auto-Visio-Helper

> Turn research-figure ideas, screenshots, and sketches into editable Microsoft Visio `.vsdx` diagrams.

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Codex Skill](https://img.shields.io/badge/Codex-Skill-blue)
![Visio](https://img.shields.io/badge/Microsoft-Visio-3955A3)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB)
![GitHub Repo stars](https://img.shields.io/github/stars/0Antique/Auto-Visio-Helper?style=social)

![Auto-Visio-Helper poster](assets/auto-visio-helper-poster-image2.png)

**Auto-Visio-Helper** is a Codex skill for planning, generating, reproducing, and refining editable Microsoft Visio scientific diagrams. Instead of asking AI to draw shapes directly and unpredictably, it first converts your natural-language request, paper screenshot, PPT screenshot, or hand-drawn sketch into a reviewable JSON drawing spec, then renders the confirmed spec into an editable `.vsdx` file through local Microsoft Visio automation.

中文文档见 [README.md](README.md).

## Why This Exists

- AI-generated diagrams often look good, but end up as flat images that cannot be edited.
- Rebuilding paper figures in Visio by hand takes too much time.
- Research diagrams usually need several revision rounds, so editable source files matter.
- Codex performs better when diagram generation is split into a spec-first workflow.

## Highlights

- **Editable by default**: outputs Visio shapes, connectors, text boxes, layers, and named objects instead of flattened screenshots.
- **Spec-first workflow**: creates a JSON drawing spec before rendering, so layout and structure can be reviewed.
- **Research-friendly patterns**: supports model architectures, method workflows, system architectures, experiment flows, concept figures, sequence diagrams, and module interaction diagrams.
- **Reference image reproduction**: redraws paper screenshots, PPT screenshots, and sketches as editable Visio diagrams.
- **Local Visio automation**: uses `scripts/render_visio.py` to render JSON specs through Microsoft Visio COM automation.
- **Preview and iteration**: supports dry-run validation and `.png` preview exports before final delivery.

## Gallery

### Max Pooling Diagram

| User request / reference input | Auto-Visio-Helper output |
| --- | --- |
| ![max pooling prompt](assets/1780674451366.png) | ![max pooling demo](demo/max_pooling_demo.png) |

### YOLO Architecture Reproduction

| Reference | Editable Visio reproduction |
| --- | --- |
| ![YOLO reference](assets/1780678594787.png) | ![YOLO architecture](assets/yolo11_architecture.png) |

### Technical Architecture Reproduction

| Reference | Editable Visio reproduction |
| --- | --- |
| ![technical architecture reference](assets/1780678953352.png) | ![technical architecture](assets/tech_architecture.png) |

## Good Fits

- Research method diagrams, framework diagrams, and technical roadmaps.
- YOLO, Transformer, CNN, encoder-decoder, detection head, and attention-module diagrams.
- Data processing, training, inference, evaluation, and deployment workflows.
- Software system architectures and module interaction diagrams.
- Experiment design, ablation studies, and benchmark comparison flows.
- Redrawing existing images into editable Visio diagrams for papers, theses, and presentations.

## Workflow

```mermaid
flowchart LR
    A["Text request / reference image"] --> B["Codex analyzes diagram type and layout"]
    B --> C["Generate JSON drawing spec"]
    C --> D["User reviews structure, style, and exports"]
    D --> E["Render editable .vsdx with local Visio"]
    E --> F["Export PNG preview"]
    F --> G["Inspect and iterate until publication-ready"]
```

## Installation

Clone this repository into your Codex skills directory:

```powershell
git clone https://github.com/0Antique/Auto-Visio-Helper.git $env:USERPROFILE\.codex\skills\auto-visio-helper
```

Then restart Codex or reload skills if your environment requires it.

## Skill Invocation Example

```text
Use $auto-visio-helper to create an editable Visio diagram for my YOLO11 pest detection method.
Include dataset preprocessing, backbone, feature fusion, detection head, loss, and output prediction.
Use a clean paper-style layout and export a PNG preview.
```

## Script Usage

Validate a drawing spec without opening Visio:

```powershell
python scripts\render_visio.py spec.json --dry-run
```

Render an editable Visio file and export a preview:

```powershell
python scripts\render_visio.py spec.json --output output\diagram.vsdx --export-png output\diagram.png
```

Render with the included Visio template:

```powershell
python scripts\render_visio.py spec.json --template references\绘图模版.vsdx --output output\diagram.vsdx --export-png output\diagram.png
```

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

## Drawing Spec Example

Auto-Visio-Helper uses JSON as the contract between Codex reasoning and Visio automation:

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

See [references/drawing_spec.md](references/drawing_spec.md) for the full spec notes.

## Directory Structure

```text
Auto-Visio-Helper/
├── SKILL.md
├── README.md
├── README-EN.md
├── agents/
│   └── openai.yaml
├── assets/
│   ├── auto-visio-helper-poster-image2.png
│   └── ...
├── demo/
│   ├── max_pooling_demo.vsdx
│   ├── yolo11_architecture.vsdx
│   └── tech_architecture.vsdx
├── references/
│   ├── diagram_types.md
│   ├── drawing_spec.md
│   ├── style_guide.md
│   ├── visio_automation.md
│   └── 绘图模版.vsdx
└── scripts/
    └── render_visio.py
```

## Design Principles

- The final diagram must stay editable; do not paste a bitmap as the final output.
- Complex diagrams should be planned as specs before rendering.
- Publication diagrams should prioritize readability, alignment, spacing, font size, and black-white print clarity.
- Reference reproduction should preserve meaning and structure while allowing publication-friendly cleanup.

## Roadmap

- More Visio shape master mappings.
- More complete `.pdf` and `.svg` export support.
- Spec templates for common model architectures.
- Stronger reference-image parsing and layout correction.

## Star History

If this project helps you turn research diagrams from pasted screenshots into editable, reusable, publication-ready Visio files, a Star would help others discover it.

[![Star History Chart](https://api.star-history.com/svg?repos=0Antique/Auto-Visio-Helper&type=Date)](https://star-history.com/#0Antique/Auto-Visio-Helper&Date)

## License

MIT License
