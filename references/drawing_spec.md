# Drawing Spec

Use this JSON spec as the contract between reasoning and Visio automation. The spec should be readable enough for the user to review before Visio is opened.

## Coordinate System

- Use millimeters.
- `x_mm` and `y_mm` are top-left coordinates.
- `width_mm` and `height_mm` define editable shape bounds.
- Keep page margins around 8-12 mm for paper figures unless a strict reference image requires otherwise.

## Top-Level Fields

```json
{
  "page": {
    "width_mm": 297,
    "height_mm": 210,
    "unit": "mm",
    "title": "Method overview"
  },
  "style": {
    "font": "Arial",
    "font_size_pt": 9,
    "theme": "paper_clean",
    "fill": "#FFFFFF",
    "line": "#2F3437",
    "line_width_pt": 1
  },
  "nodes": [],
  "edges": [],
  "groups": [],
  "annotations": [],
  "exports": {"png": true, "pdf": false, "svg": false}
}
```

## Nodes

Each node must have a stable `id`, label, position, and size.

```json
{
  "id": "backbone",
  "label": "Backbone\nC2f + SPPF",
  "shape": "rounded_rectangle",
  "x_mm": 28,
  "y_mm": 52,
  "width_mm": 48,
  "height_mm": 24,
  "fill": "#EAF2FF",
  "line": "#245CA8",
  "layer": "model",
  "group": "YOLO pipeline"
}
```

Supported initial shapes for `scripts/render_visio.py`:

- `rectangle`
- `rounded_rectangle`
- `ellipse`
- `diamond`
- `parallelogram`

Prefer rectangles or rounded rectangles for model blocks, parallelograms for input/output, diamonds for decisions, and ellipses only for start/end or compact concept nodes.

## Edges

Edges connect node IDs. Use explicit labels only when the meaning is not obvious.

```json
{
  "id": "e_input_backbone",
  "from": "input",
  "to": "backbone",
  "label": "feature extraction",
  "arrow": "end",
  "line": "#2F3437",
  "layer": "connections"
}
```

Use left-to-right flow for model architectures and top-to-bottom flow for process diagrams unless the user or source image says otherwise.

## Groups

Groups describe conceptual regions. The renderer may create editable containers in a later version; for now, use them to drive layout and layer naming.

```json
{
  "id": "training",
  "label": "Training stage",
  "node_ids": ["dataset", "augmentation", "loss"],
  "style": "subtle_container"
}
```

## Annotations

Use annotations for legends, callouts, equations, and short explanatory notes.

```json
{
  "id": "note_loss",
  "text": "Loss = box + cls + dfl",
  "x_mm": 184,
  "y_mm": 126,
  "width_mm": 54,
  "height_mm": 12,
  "layer": "annotations"
}
```

## Minimal Example

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
