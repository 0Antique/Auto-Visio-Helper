import json
from pathlib import Path

S = 0.2
PAGE_W = 320
PAGE_H = 180

COLORS = {
    "bg": "#F6F8FB",
    "ink": "#1F2937",
    "muted": "#5D6675",
    "white": "#FFFFFF",
    "line": "#D9E1EC",
    "dark": "#1F2937",
    "cap_bg": "#EEF7FF",
    "cap_line": "#B8D9F5",
    "hi_bg": "#FFF7EC",
    "hi_line": "#F2D19D",
    "flow_bg": "#F4F7FB",
    "icon_blue": "#DBEAFE",
    "icon_green": "#E5F6EA",
    "icon_purple": "#EFE7FF",
    "icon_orange": "#FFEDD5",
}


def mm(v):
    return round(v * S, 3)


def node(node_id, label, x, y, w, h, fill, line=None, fs=10, text="#1F2937", shape="rounded_rectangle", layer="poster"):
    return {
        "id": node_id,
        "label": label,
        "shape": shape,
        "x_mm": mm(x),
        "y_mm": mm(y),
        "width_mm": mm(w),
        "height_mm": mm(h),
        "fill": fill,
        "line": line or fill,
        "line_width_pt": 0.8,
        "font_size_pt": fs,
        "text_color": text,
        "corner_radius_mm": 2.0,
        "layer": layer,
    }


def txt(text_id, text, x, y, w, h, fs=10, color="#1F2937"):
    return {
        "id": text_id,
        "text": text,
        "x_mm": mm(x),
        "y_mm": mm(y),
        "width_mm": mm(w),
        "height_mm": mm(h),
        "font_size_pt": fs,
        "text_color": color,
        "layer": "text",
    }


def line(line_id, pts, arrow="end", color="#667085", lw=1.4):
    return {
        "id": line_id,
        "points_mm": [{"x": mm(x), "y": mm(y)} for x, y in pts],
        "arrow": arrow,
        "line": color,
        "line_width_pt": lw,
        "layer": "connections",
    }


nodes = []
annotations = []
lines = []

nodes.append(node("page_bg", "", 0, 0, 1600, 900, COLORS["bg"], COLORS["bg"], shape="rectangle", layer="background"))

# Header.
nodes.append(node("header", "", 70, 54, 1460, 116, COLORS["white"], COLORS["line"], layer="header"))
annotations.extend(
    [
        txt("main_title", "Auto-Visio-Helper", 110, 70, 460, 44, 24, COLORS["ink"]),
        txt("subtitle", "把模糊科研绘图需求转成可检查、可复现、可编辑的 Microsoft Visio 图", 112, 124, 900, 32, 13, COLORS["muted"]),
    ]
)
nodes.append(node("header_badge", "JSON spec → VSDX", 1210, 82, 270, 54, COLORS["dark"], COLORS["dark"], 10, COLORS["white"], layer="header"))

# Panels.
panel_specs = [
    ("cap_panel", 70, 210, 445, 530, COLORS["cap_bg"], COLORS["cap_line"], "核心能力", "从需求理解到结构化复刻"),
    ("flow_panel", 555, 210, 490, 530, COLORS["flow_bg"], COLORS["line"], "工作流", "先规划，再渲染，最后导出预览"),
    ("hi_panel", 1085, 210, 445, 530, COLORS["hi_bg"], COLORS["hi_line"], "实现亮点", "让图可确认、可编辑、可导出、可复用"),
]
for pid, x, y, w, h, fill, border, title, subtitle in panel_specs:
    nodes.append(node(pid, "", x, y, w, h, fill, border, layer="panels"))
    annotations.append(txt(f"{pid}_title", title, x + 32, y + 28, 170, 32, 17, COLORS["ink"]))
    annotations.append(txt(f"{pid}_subtitle", subtitle, x + 34, y + 70, 290, 22, 9, COLORS["muted"]))

# Capability cards.
cap_cards = [
    ("cap_plan", 98, 330, "绘图方案整理", "把模糊科研需求整理成\n清晰、可检查的绘图方案", COLORS["icon_blue"], "≡"),
    ("cap_nl", 98, 462, "自然语言生成图", "模型结构图、方法流程图\n系统架构图、实验流程图", COLORS["icon_green"], "▾"),
    ("cap_ref", 98, 594, "参考图可编辑复现", "论文截图、手绘草图、PPT 截图\n在 Visio 中重建为可编辑图形", COLORS["icon_purple"], "△"),
]
for cid, x, y, title, body, icon_color, icon_text in cap_cards:
    nodes.append(node(f"{cid}_card", "", x, y, 389, 112, COLORS["white"], COLORS["line"], layer="cards"))
    nodes.append(node(f"{cid}_icon", icon_text, x + 20, y + 24, 66, 64, icon_color, "#7AADE8", 18, COLORS["ink"], layer="icons"))
    annotations.append(txt(f"{cid}_title", title, x + 104, y + 24, 260, 28, 12, COLORS["ink"]))
    annotations.append(txt(f"{cid}_body", body, x + 104, y + 58, 260, 48, 9, COLORS["muted"]))

# Flow.
nodes.append(node("flow_input", "用户输入\n自然语言 / 参考图片", 599, 332, 180, 78, COLORS["white"], "#98A5B7", 11, COLORS["ink"], layer="flow"))
nodes.append(node("flow_spec", "绘图规格\ndrawing_spec.json", 871, 332, 180, 78, "#E7F5FF", "#65A9D8", 11, COLORS["ink"], layer="flow"))
nodes.append(node("flow_com", "Visio COM\n自动放置形状与连线", 599, 448, 180, 78, "#EAF7ED", "#66A974", 11, COLORS["ink"], layer="flow"))
nodes.append(node("flow_output", "可编辑输出\n.vsdx + .png", 871, 448, 180, 78, "#FFF0E2", "#E19A45", 11, COLORS["ink"], layer="flow"))
nodes.append(node("flow_principle", "核心原则\n不粘贴整张截图，而是重建 Visio 原生图元", 605, 600, 400, 78, COLORS["white"], COLORS["line"], 10, COLORS["ink"], layer="flow"))
lines.extend(
    [
        line("flow_arrow_1", [(789, 371), (860, 371)]),
        line("flow_arrow_2", [(789, 487), (860, 487)]),
        line("flow_down", [(800, 410), (800, 448)]),
    ]
)

# Highlight cards.
hi_cards = [
    ("hi_json", 1113, 326, "先生成 JSON drawing spec", "用户确认后再调用 Visio 绘图", COLORS["icon_orange"], "{ }"),
    ("hi_edit", 1113, 428, "真正可编辑的 Visio 元素", "形状、连接线、文本框、图层、命名对象", COLORS["icon_green"], "□"),
    ("hi_export", 1113, 530, "预览与多格式导出", "支持 .png，预留 .pdf / .svg 导出能力", COLORS["icon_blue"], "▣"),
    ("hi_ref", 1113, 632, "内置科研绘图参考", "论文风格、布局模式、Visio 自动化文档", COLORS["icon_purple"], "⌒"),
]
for cid, x, y, title, body, icon_color, icon_text in hi_cards:
    nodes.append(node(f"{cid}_card", "", x, y, 389, 86, COLORS["white"], COLORS["line"], layer="cards"))
    nodes.append(node(f"{cid}_icon", icon_text, x + 20, y + 18, 54, 50, icon_color, "#E8A146", 14, COLORS["ink"], layer="icons"))
    annotations.append(txt(f"{cid}_title", title, x + 94, y + 18, 280, 28, 11, COLORS["ink"]))
    annotations.append(txt(f"{cid}_body", body, x + 94, y + 54, 280, 24, 9, COLORS["muted"]))

# Footer.
nodes.append(
    node(
        "footer",
        "vague request / reference image → reviewable JSON spec → Visio COM automation → editable VSDX + preview exports",
        96,
        792,
        1408,
        56,
        COLORS["dark"],
        COLORS["dark"],
        9,
        COLORS["white"],
        layer="footer",
    )
)

spec = {
    "page": {"width_mm": PAGE_W, "height_mm": PAGE_H, "unit": "mm", "title": "Auto-Visio-Helper Poster"},
    "style": {
        "font": "Microsoft YaHei",
        "font_size_pt": 9,
        "theme": "paper_clean",
        "fill": COLORS["white"],
        "line": COLORS["line"],
        "text_color": COLORS["ink"],
        "line_width_pt": 0.8,
    },
    "nodes": nodes,
    "edges": [],
    "lines": lines,
    "groups": [],
    "annotations": annotations,
    "exports": {"png": True, "pdf": False, "svg": False},
}

Path("assets/auto-visio-helper-poster-vsdx-spec.json").write_text(
    json.dumps(spec, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
