import json
from pathlib import Path

PAGE_W = 220
PAGE_H = 125

COLORS = {
    "line": "#2F3437",
    "title": "#F1F3F5",
    "window_a": "#FFF3D6",
    "window_b": "#DCE9FA",
    "window_c": "#E8F3E8",
    "window_d": "#FCE8E6",
    "output": "#FFFFFF",
    "note": "#F6F7F8",
}


def rect(node_id, label, x, y, w, h, fill, line=None, fs=10, layer="model"):
    return {
        "id": node_id,
        "label": label,
        "shape": "rectangle",
        "x_mm": x,
        "y_mm": y,
        "width_mm": w,
        "height_mm": h,
        "fill": fill,
        "line": line or COLORS["line"],
        "line_width_pt": 0.9,
        "font_size_pt": fs,
        "layer": layer,
    }


def rounded(node_id, label, x, y, w, h, fill, line=None, fs=10, layer="model"):
    item = rect(node_id, label, x, y, w, h, fill, line, fs, layer)
    item["shape"] = "rounded_rectangle"
    item["corner_radius_mm"] = 1.5
    return item


def text(text_id, value, x, y, w, h, fs=9):
    return {
        "id": text_id,
        "text": value,
        "x_mm": x,
        "y_mm": y,
        "width_mm": w,
        "height_mm": h,
        "font_size_pt": fs,
        "layer": "annotations",
    }


def line(line_id, points, arrow="end"):
    return {
        "id": line_id,
        "points_mm": [{"x": x, "y": y} for x, y in points],
        "arrow": arrow,
        "line": COLORS["line"],
        "line_width_pt": 1.0,
        "layer": "connections",
    }


nodes = [
    rounded("title", "Max Pooling / 最大池化示意图", 55, 8, 110, 12, COLORS["title"], "#CED4DA", 13, "title"),
    rounded("params", "Kernel = 2 x 2     Stride = 2     Operation = max", 57, 24, 106, 9, COLORS["note"], "#CED4DA", 8, "annotations"),
    rounded("operation", "2 x 2 Max\nPooling", 92, 58, 38, 20, COLORS["note"], "#868E96", 9, "operation"),
]
annotations = [
    text("input_label", "Input feature map (4 x 4)", 21, 35, 55, 6, 9),
    text("output_label", "Output feature map (2 x 2)", 151, 35, 55, 6, 9),
]
lines = []

input_values = [
    [1, 3, 2, 4],
    [5, 6, 1, 2],
    [7, 2, 8, 3],
    [1, 4, 6, 9],
]
output_values = [
    [6, 4],
    [7, 9],
]
window_fills = [
    [COLORS["window_a"], COLORS["window_a"], COLORS["window_b"], COLORS["window_b"]],
    [COLORS["window_a"], COLORS["window_a"], COLORS["window_b"], COLORS["window_b"]],
    [COLORS["window_c"], COLORS["window_c"], COLORS["window_d"], COLORS["window_d"]],
    [COLORS["window_c"], COLORS["window_c"], COLORS["window_d"], COLORS["window_d"]],
]
output_fills = [
    [COLORS["window_a"], COLORS["window_b"]],
    [COLORS["window_c"], COLORS["window_d"]],
]

cell = 13
gap = 1
input_x = 22
input_y = 44
output_x = 162
output_y = 51

for r, row in enumerate(input_values):
    for c, value in enumerate(row):
        nodes.append(
            rect(
                f"in_{r}_{c}",
                str(value),
                input_x + c * (cell + gap),
                input_y + r * (cell + gap),
                cell,
                cell,
                window_fills[r][c],
                fs=11,
                layer="input",
            )
        )

for r, row in enumerate(output_values):
    for c, value in enumerate(row):
        nodes.append(
            rect(
                f"out_{r}_{c}",
                str(value),
                output_x + c * (cell + gap),
                output_y + r * (cell + gap),
                cell,
                cell,
                output_fills[r][c],
                fs=12,
                layer="output",
            )
        )

nodes.extend(
    [
        rounded("formula_a", "max(1, 3, 5, 6) = 6", 6, 103, 48, 9, COLORS["window_a"], "#D8B35A", 6.2, "formula"),
        rounded("formula_b", "max(2, 4, 1, 2) = 4", 59, 103, 48, 9, COLORS["window_b"], "#729BD7", 6.2, "formula"),
        rounded("formula_c", "max(7, 2, 1, 4) = 7", 112, 103, 48, 9, COLORS["window_c"], "#80A982", 6.2, "formula"),
        rounded("formula_d", "max(8, 3, 6, 9) = 9", 165, 103, 48, 9, COLORS["window_d"], "#D58A8A", 6.2, "formula"),
    ]
)

lines.extend(
    [
        line("input_to_operation", [(80, 70), (92, 70)]),
        line("operation_to_output", [(130, 70), (162, 70)]),
    ]
)

spec = {
    "page": {"width_mm": PAGE_W, "height_mm": PAGE_H, "unit": "mm", "title": "Max Pooling Demo"},
    "style": {
        "font": "Arial",
        "font_size_pt": 9,
        "theme": "paper_clean",
        "fill": "#FFFFFF",
        "line": COLORS["line"],
        "line_width_pt": 0.9,
    },
    "nodes": nodes,
    "edges": [],
    "lines": lines,
    "groups": [],
    "annotations": annotations,
    "exports": {"png": True, "pdf": False, "svg": False},
}

Path("demo/max_pooling_demo_spec.json").write_text(
    json.dumps(spec, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
