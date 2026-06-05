import json
from pathlib import Path

W = 282
H = 250

COLORS = {
    "cbs": "#F6D9A8",
    "c3k2": "#A9DEE3",
    "purple": "#D8B4DE",
    "upsample": "#F1C1D7",
    "contact": "#C6E0C5",
    "dsc": "#DCE9FA",
    "conv": "#F6C8C8",
    "white": "#FFFFFF",
    "black": "#111111",
    "red": "#E10F00",
    "green": "#8ED357",
    "blue": "#8EA3DE",
}


def node(node_id, label, x, y, w, h, fill, line=None, shape="rectangle", fs=8.5, layer="model"):
    return {
        "id": node_id,
        "label": label,
        "shape": shape,
        "x_mm": x,
        "y_mm": y,
        "width_mm": w,
        "height_mm": h,
        "fill": fill,
        "line": line or COLORS["black"],
        "line_width_pt": 0.7,
        "font_size_pt": fs,
        "layer": layer,
    }


def text(text_id, value, x, y, w, h, fs=7.5):
    return {
        "id": text_id,
        "text": value,
        "x_mm": x,
        "y_mm": y,
        "width_mm": w,
        "height_mm": h,
        "font_size_pt": fs,
        "layer": "labels",
    }


def line(line_id, points, arrow="end", lw=0.7):
    return {
        "id": line_id,
        "points_mm": [{"x": x, "y": y} for x, y in points],
        "arrow": arrow,
        "line": COLORS["black"],
        "line_width_pt": lw,
        "layer": "connections",
    }


nodes = []
annotations = []
lines = []

nodes.extend(
    [
        node("box_backbone", "", 9, 3, 36, 214, COLORS["white"], shape="rounded_rectangle", layer="containers"),
        node("box_neck", "", 57, 3, 90, 160, COLORS["white"], shape="rounded_rectangle", layer="containers"),
        node("box_head", "", 147, 3, 132, 160, COLORS["white"], shape="rounded_rectangle", layer="containers"),
    ]
)
annotations.extend(
    [
        text("title_backbone", "Backbone", 17, 7, 25, 8, 10),
        text("title_neck", "Neck", 99, 7, 24, 8, 10),
        text("title_head", "Head", 246, 5, 24, 8, 10),
    ]
)

# Backbone.
bx, bw, bh = 14, 27, 10
backbone = [
    ("b0", "CBS", 203, COLORS["cbs"], "0", "3x640x640"),
    ("b1", "CBS", 184, COLORS["cbs"], "1", "16x320x320"),
    ("b2", "C3K2", 165, COLORS["c3k2"], "2", "32x160x160"),
    ("b3", "CBS", 146, COLORS["cbs"], "3", "32x160x160"),
    ("b4", "C3K2", 127, COLORS["c3k2"], "4", "64x80x80"),
    ("b5", "CBS", 108, COLORS["cbs"], "5", "64x80x80"),
    ("b6", "C3K2", 89, COLORS["c3k2"], "6", "128x40x40"),
    ("b7", "CBS", 70, COLORS["cbs"], "7", "128x40x40"),
    ("b8", "C3K2", 51, COLORS["c3k2"], "8", "256x20x20"),
    ("b9", "SPPF", 33, COLORS["purple"], "9", "256x20x20"),
    ("b10", "C2PSA", 17, COLORS["purple"], "10", "256x20x20"),
]
for node_id, label, y, fill, idx, dim in backbone:
    nodes.append(node(node_id, label, bx, y, bw, bh, fill, fs=8.5))
    annotations.append(text(f"idx_{idx}", idx, 4, y + 2, 6, 5, 7))
    annotations.append(text(f"dim_{node_id}", dim, bx + 16, y + bh + 1, 22, 4, 6))
for i in range(len(backbone) - 1):
    a, _, y1, *_ = backbone[i]
    b, _, y2, *_ = backbone[i + 1]
    lines.append(line(f"bb_{a}_{b}", [(bx + bw / 2, y1), (bx + bw / 2, y2 + bh)]))

# Input icon.
nodes.extend(
    [
        node("input_blue", "", 18, 223, 19, 17, COLORS["blue"], COLORS["blue"], fs=1),
        node("input_green", "", 16, 227, 19, 17, COLORS["green"], COLORS["green"], fs=1),
        node("input_red", "", 14, 231, 19, 17, COLORS["red"], COLORS["red"], fs=1),
    ]
)

# Neck left column.
neck_left_x = 63
neck_w = 27
neck_left = [
    ("n11", "Upsample", 27, COLORS["upsample"], "11", "256x40x40"),
    ("n12", "Contact", 44, COLORS["contact"], "12", "384x40x40"),
    ("n13", "C3K2", 70, COLORS["c3k2"], "13", "128x40x40"),
    ("n14", "Upsample", 94, COLORS["upsample"], "14", "128x80x80"),
    ("n15", "Contact", 119, COLORS["contact"], "15", "192x80x80"),
]
for node_id, label, y, fill, idx, dim in neck_left:
    nodes.append(node(node_id, label, neck_left_x, y, neck_w, bh, fill, fs=7.8))
    annotations.append(text(f"idx_{idx}", idx, neck_left_x - 6, y + 2, 6, 5, 7))
    annotations.append(text(f"dim_{node_id}", dim, neck_left_x + 15, y + bh + 1, 22, 4, 6))
for a, b in [("n11", "n12"), ("n12", "n13"), ("n13", "n14"), ("n14", "n15")]:
    ya = next(y for nid, _, y, *_ in neck_left if nid == a)
    yb = next(y for nid, _, y, *_ in neck_left if nid == b)
    lines.append(line(f"{a}_{b}", [(neck_left_x + neck_w / 2, ya + bh), (neck_left_x + neck_w / 2, yb)]))

# Neck right column.
neck_right_x = 113
neck_right = [
    ("n16", "C3K2", 138, COLORS["c3k2"], "16", "64x80x80"),
    ("n17", "CBS", 119, COLORS["cbs"], "17", "64x40x40"),
    ("n18", "Contact", 101, COLORS["contact"], "18", "192x40x40"),
    ("n19", "C3K2", 83, COLORS["c3k2"], "19", "128x40x40"),
    ("n20", "CBS", 65, COLORS["cbs"], "20", "128x20x20"),
    ("n21", "Contact", 44, COLORS["contact"], "21", "384x20x20"),
    ("n22", "C3K2", 26, COLORS["c3k2"], "22", "256x20x20"),
]
for node_id, label, y, fill, idx, dim in neck_right:
    nodes.append(node(node_id, label, neck_right_x, y, neck_w, bh, fill, fs=7.8))
    annotations.append(text(f"idx_{idx}", idx, neck_right_x + neck_w + 1, y + 2, 6, 5, 7))
    annotations.append(text(f"dim_{node_id}", dim, neck_right_x + 14, y - 5, 24, 4, 6))
for a, b in [("n16", "n17"), ("n17", "n18"), ("n18", "n19"), ("n19", "n20"), ("n20", "n21"), ("n21", "n22")]:
    ya = next(y for nid, _, y, *_ in neck_right if nid == a)
    yb = next(y for nid, _, y, *_ in neck_right if nid == b)
    lines.append(line(f"{a}_{b}", [(neck_right_x + neck_w / 2, ya), (neck_right_x + neck_w / 2, yb + bh)]))

# Cross-stage feature routes.
lines.extend(
    [
        line("route_b10_n11", [(bx + bw, 22, ), (51, 22), (51, 32), (neck_left_x, 32)]),
        line("route_b8_n21", [(bx + bw, 56), (98, 56), (98, 49), (neck_right_x, 49)]),
        line("route_b6_n12", [(bx + bw, 94), (53, 94), (53, 49), (neck_left_x, 49)]),
        line("route_b4_n15", [(bx + bw, 132), (53, 132), (53, 124), (neck_left_x, 124)]),
        line("route_n13_n18", [(neck_left_x + neck_w, 75), (101, 75), (101, 106), (neck_right_x, 106)]),
        line("route_n15_n16", [(neck_left_x + neck_w / 2, 143), (108, 143), (108, 143), (neck_right_x, 143)]),
    ]
)

# Head blocks: three scales, two branches per scale.
def head_row(prefix, y, source_id):
    x1, x2, x3 = 165, 202, 238
    nodes.extend(
        [
            node(f"{prefix}_cbs1", "CBS", x1, y, 27, 10, COLORS["cbs"], fs=8.5),
            node(f"{prefix}_cbs2", "CBS", x2, y, 27, 10, COLORS["cbs"], fs=8.5),
            node(f"{prefix}_conv1", "Conv2d", x3, y, 25, 10, COLORS["conv"], "#D05C5C", fs=8),
            node(f"{prefix}_dsc1", "DSC", x1, y + 19, 27, 10, COLORS["dsc"], "#729BD7", fs=8.5),
            node(f"{prefix}_dsc2", "DSC", x2, y + 19, 27, 10, COLORS["dsc"], "#729BD7", fs=8.5),
            node(f"{prefix}_conv2", "Conv2d", x3, y + 19, 25, 10, COLORS["conv"], "#D05C5C", fs=8),
        ]
    )
    source_y = {"n22": 31, "n19": 88, "n16": 143}[source_id]
    lines.extend(
        [
            line(f"{prefix}_src_top", [(147, source_y), (152, source_y), (152, y + 5), (x1, y + 5)]),
            line(f"{prefix}_src_bottom", [(147, source_y), (152, source_y), (152, y + 24), (x1, y + 24)]),
            line(f"{prefix}_cbs", [(x1 + 27, y + 5), (x2, y + 5)]),
            line(f"{prefix}_cbs_conv", [(x2 + 27, y + 5), (x3, y + 5)]),
            line(f"{prefix}_dsc", [(x1 + 27, y + 24), (x2, y + 24)]),
            line(f"{prefix}_dsc_conv", [(x2 + 27, y + 24), (x3, y + 24)]),
        ]
    )


head_row("h20", 16, "n22")
head_row("h40", 72, "n19")
head_row("h80", 127, "n16")

spec = {
    "page": {"width_mm": W, "height_mm": H, "unit": "mm", "title": "YOLO11 Architecture"},
    "style": {
        "font": "Arial",
        "font_size_pt": 8,
        "theme": "paper_clean",
        "fill": "#FFFFFF",
        "line": COLORS["black"],
        "line_width_pt": 0.7,
    },
    "nodes": nodes,
    "edges": [],
    "lines": lines,
    "groups": [],
    "annotations": annotations,
    "exports": {"png": True, "pdf": False, "svg": False},
}

Path("demo/yolo11_architecture_spec.json").write_text(
    json.dumps(spec, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
