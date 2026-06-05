#!/usr/bin/env python3
"""Render an Auto Visio Helper drawing spec to an editable Visio document.

The script validates JSON specs in dry-run mode without requiring Visio or
pywin32. Rendering mode requires Windows, Microsoft Visio, and pywin32.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

MM_PER_INCH = 25.4

SHAPE_MASTERS = {
    "rectangle": "Rectangle",
    "rounded_rectangle": "Rounded Rectangle",
    "ellipse": "Ellipse",
    "diamond": "Diamond",
    "parallelogram": "Parallelogram",
}


class SpecError(ValueError):
    """Raised when the drawing spec is invalid."""


def mm_to_in(value: float) -> float:
    return float(value) / MM_PER_INCH


def load_spec(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        spec = json.load(handle)
    if not isinstance(spec, dict):
        raise SpecError("Top-level spec must be a JSON object.")
    return spec


def require_number(obj: dict[str, Any], key: str, context: str) -> float:
    value = obj.get(key)
    if not isinstance(value, (int, float)):
        raise SpecError(f"{context}.{key} must be a number.")
    return float(value)


def validate_spec(spec: dict[str, Any]) -> None:
    page = spec.get("page")
    if not isinstance(page, dict):
        raise SpecError("page must be an object.")
    require_number(page, "width_mm", "page")
    require_number(page, "height_mm", "page")

    nodes = spec.get("nodes")
    if not isinstance(nodes, list) or not nodes:
        raise SpecError("nodes must be a non-empty list.")

    seen: set[str] = set()
    for index, node in enumerate(nodes):
        if not isinstance(node, dict):
            raise SpecError(f"nodes[{index}] must be an object.")
        node_id = node.get("id")
        if not isinstance(node_id, str) or not node_id.strip():
            raise SpecError(f"nodes[{index}].id must be a non-empty string.")
        if node_id in seen:
            raise SpecError(f"Duplicate node id: {node_id}")
        seen.add(node_id)
        if not isinstance(node.get("label", ""), str):
            raise SpecError(f"Node {node_id}.label must be a string.")
        for key in ("x_mm", "y_mm", "width_mm", "height_mm"):
            require_number(node, key, f"node {node_id}")
        shape = node.get("shape", "rounded_rectangle")
        if shape not in SHAPE_MASTERS:
            allowed = ", ".join(sorted(SHAPE_MASTERS))
            raise SpecError(f"Node {node_id}.shape must be one of: {allowed}")

    edges = spec.get("edges", [])
    if not isinstance(edges, list):
        raise SpecError("edges must be a list when present.")
    for index, edge in enumerate(edges):
        if not isinstance(edge, dict):
            raise SpecError(f"edges[{index}] must be an object.")
        edge_id = edge.get("id", f"edges[{index}]")
        source = edge.get("from")
        target = edge.get("to")
        if source not in seen:
            raise SpecError(f"Edge {edge_id} references missing source node: {source}")
        if target not in seen:
            raise SpecError(f"Edge {edge_id} references missing target node: {target}")

    annotations = spec.get("annotations", [])
    if not isinstance(annotations, list):
        raise SpecError("annotations must be a list when present.")
    for index, annotation in enumerate(annotations):
        if not isinstance(annotation, dict):
            raise SpecError(f"annotations[{index}] must be an object.")
        for key in ("x_mm", "y_mm", "width_mm", "height_mm"):
            require_number(annotation, key, f"annotation {annotation.get('id', index)}")

    lines = spec.get("lines", [])
    if not isinstance(lines, list):
        raise SpecError("lines must be a list when present.")
    for index, line in enumerate(lines):
        if not isinstance(line, dict):
            raise SpecError(f"lines[{index}] must be an object.")
        points = line.get("points_mm")
        if not isinstance(points, list) or len(points) < 2:
            raise SpecError(f"line {line.get('id', index)}.points_mm must contain at least two points.")
        for point_index, point in enumerate(points):
            if not isinstance(point, dict):
                raise SpecError(f"line {line.get('id', index)}.points_mm[{point_index}] must be an object.")
            require_number(point, "x", f"line {line.get('id', index)} point {point_index}")
            require_number(point, "y", f"line {line.get('id', index)} point {point_index}")


def top_left_to_visio(page_height_mm: float, item: dict[str, Any]) -> tuple[float, float, float, float]:
    width_mm = float(item["width_mm"])
    height_mm = float(item["height_mm"])
    center_x_mm = float(item["x_mm"]) + width_mm / 2
    center_y_mm = page_height_mm - float(item["y_mm"]) - height_mm / 2
    return (
        mm_to_in(center_x_mm),
        mm_to_in(center_y_mm),
        mm_to_in(width_mm),
        mm_to_in(height_mm),
    )


def edge_points(
    source: tuple[float, float, float, float],
    target: tuple[float, float, float, float],
) -> tuple[float, float, float, float]:
    source_x, source_y, source_w, source_h = source
    target_x, target_y, target_w, target_h = target
    dx = target_x - source_x
    dy = target_y - source_y

    if abs(dx) >= abs(dy):
        if dx >= 0:
            start_x = source_x + source_w / 2
            end_x = target_x - target_w / 2
        else:
            start_x = source_x - source_w / 2
            end_x = target_x + target_w / 2
        return start_x, source_y, end_x, target_y

    if dy >= 0:
        start_y = source_y + source_h / 2
        end_y = target_y - target_h / 2
    else:
        start_y = source_y - source_h / 2
        end_y = target_y + target_h / 2
    return source_x, start_y, target_x, end_y


def set_cell(shape: Any, cell_name: str, formula: str) -> None:
    shape.CellsU(cell_name).FormulaU = formula


def apply_shape_style(shape: Any, node: dict[str, Any], style: dict[str, Any]) -> None:
    fill = node.get("fill", style.get("fill", "#FFFFFF"))
    line = node.get("line", style.get("line", "#2F3437"))
    line_width = node.get("line_width_pt", style.get("line_width_pt", 1))
    font = node.get("font", style.get("font", "Arial"))
    font_size = node.get("font_size_pt", style.get("font_size_pt", 9))
    text_color = node.get("text_color", style.get("text_color", "#1F2937"))
    corner_radius = node.get("corner_radius_mm", style.get("corner_radius_mm"))

    set_cell(shape, "FillForegnd", f"RGB({int(fill[1:3], 16)},{int(fill[3:5], 16)},{int(fill[5:7], 16)})")
    set_cell(shape, "LineColor", f"RGB({int(line[1:3], 16)},{int(line[3:5], 16)},{int(line[5:7], 16)})")
    set_cell(shape, "LineWeight", f"{float(line_width)} pt")
    if corner_radius is not None:
        radius_formula = f"{mm_to_in(float(corner_radius))} in"
        set_cell(shape, "Rounding", radius_formula)
        try:
            set_cell(shape, "Controls.X1", radius_formula)
        except Exception:
            pass
    shape.CellsU("Char.Size").FormulaU = f"{float(font_size)} pt"
    shape.CellsU("Char.Font").FormulaU = f'"{font}"'
    shape.CellsU("Char.Color").FormulaU = f"RGB({int(text_color[1:3], 16)},{int(text_color[3:5], 16)},{int(text_color[5:7], 16)})"


def get_or_create_layer(page: Any, name: str) -> Any:
    layers = page.Layers
    for index in range(1, layers.Count + 1):
        layer = layers.Item(index)
        if layer.Name == name:
            return layer
    return layers.Add(name)


def add_to_layer(page: Any, shape: Any, layer_name: str | None) -> None:
    if not layer_name:
        return
    layer = get_or_create_layer(page, layer_name)
    layer.Add(shape, 0)


def point_to_visio(page_height_mm: float, point: dict[str, Any]) -> tuple[float, float]:
    return mm_to_in(float(point["x"])), mm_to_in(page_height_mm - float(point["y"]))


def apply_line_style(shape: Any, line_spec: dict[str, Any], style: dict[str, Any], is_last: bool = True) -> None:
    line = line_spec.get("line", style.get("line", "#2F3437"))
    shape.CellsU("LineColor").FormulaU = f"RGB({int(line[1:3], 16)},{int(line[3:5], 16)},{int(line[5:7], 16)})"
    shape.CellsU("LineWeight").FormulaU = f"{float(line_spec.get('line_width_pt', style.get('line_width_pt', 1)))} pt"
    if is_last:
        shape.CellsU("EndArrow").FormulaU = "5" if line_spec.get("arrow", "end") in {"end", "both"} else "0"
    else:
        shape.CellsU("EndArrow").FormulaU = "0"
    shape.CellsU("BeginArrow").FormulaU = "5" if line_spec.get("arrow") == "both" else "0"


def render_visio(
    spec: dict[str, Any],
    output: Path,
    template: Path | None = None,
    export_png: Path | None = None,
    export_pdf: Path | None = None,
    export_svg: Path | None = None,
) -> None:
    try:
        import win32com.client  # type: ignore
    except ImportError as exc:
        raise RuntimeError("pywin32 is required for Visio rendering. Install with: python -m pip install pywin32") from exc

    page_spec = spec["page"]
    style = spec.get("style", {})
    page_width_mm = float(page_spec["width_mm"])
    page_height_mm = float(page_spec["height_mm"])

    try:
        visio = win32com.client.DispatchEx("Visio.Application")
    except AttributeError:
        visio = win32com.client.Dispatch("Visio.Application")
    visio.Visible = False

    if template:
        doc = visio.Documents.Open(str(template.resolve()))
    else:
        doc = visio.Documents.Add("")

    page = visio.ActivePage
    page.PageSheet.CellsU("PageWidth").FormulaU = f"{mm_to_in(page_width_mm)} in"
    page.PageSheet.CellsU("PageHeight").FormulaU = f"{mm_to_in(page_height_mm)} in"

    basic = visio.Documents.OpenEx("BASIC_U.VSSX", 64)

    shapes_by_id: dict[str, Any] = {}
    bounds_by_id: dict[str, tuple[float, float, float, float]] = {}

    for node in spec["nodes"]:
        pin_x, pin_y, width, height = top_left_to_visio(page_height_mm, node)
        master_name = SHAPE_MASTERS[node.get("shape", "rounded_rectangle")]
        master = basic.Masters.ItemU(master_name)
        shape = page.Drop(master, pin_x, pin_y)
        shape.Name = node["id"]
        shape.Text = node.get("label", "")
        shape.CellsU("Width").FormulaU = f"{width} in"
        shape.CellsU("Height").FormulaU = f"{height} in"
        apply_shape_style(shape, node, style)
        add_to_layer(page, shape, node.get("layer"))
        shapes_by_id[node["id"]] = shape
        bounds_by_id[node["id"]] = (pin_x, pin_y, width, height)

    for edge in spec.get("edges", []):
        source = bounds_by_id[edge["from"]]
        target = bounds_by_id[edge["to"]]
        start_x, start_y, end_x, end_y = edge_points(source, target)
        connector = page.DrawLine(start_x, start_y, end_x, end_y)
        connector.Name = edge.get("id", f"{edge['from']}_to_{edge['to']}")
        connector.CellsU("EndArrow").FormulaU = "5" if edge.get("arrow", "end") in {"end", "both"} else "0"
        connector.CellsU("BeginArrow").FormulaU = "5" if edge.get("arrow") == "both" else "0"
        line = edge.get("line", style.get("line", "#2F3437"))
        connector.CellsU("LineColor").FormulaU = f"RGB({int(line[1:3], 16)},{int(line[3:5], 16)},{int(line[5:7], 16)})"
        connector.CellsU("LineWeight").FormulaU = f"{float(edge.get('line_width_pt', style.get('line_width_pt', 1)))} pt"
        add_to_layer(page, connector, edge.get("layer"))
        if edge.get("label"):
            mid_x = (start_x + end_x) / 2
            mid_y = (start_y + end_y) / 2
            label = page.DrawRectangle(mid_x - 0.35, mid_y - 0.1, mid_x + 0.35, mid_y + 0.1)
            label.Name = f"{connector.Name}_label"
            label.Text = edge["label"]
            label.CellsU("LinePattern").FormulaU = "0"
            label.CellsU("FillPattern").FormulaU = "0"
            label.CellsU("Char.Size").FormulaU = f"{float(style.get('font_size_pt', 8))} pt"
            add_to_layer(page, label, edge.get("layer"))

    for line_spec in spec.get("lines", []):
        points = [point_to_visio(page_height_mm, point) for point in line_spec["points_mm"]]
        for index, (start, end) in enumerate(zip(points, points[1:])):
            segment = page.DrawLine(start[0], start[1], end[0], end[1])
            segment.Name = f"{line_spec.get('id', 'line')}_{index + 1}"
            apply_line_style(segment, line_spec, style, index == len(points) - 2)
            add_to_layer(page, segment, line_spec.get("layer"))

    for annotation in spec.get("annotations", []):
        pin_x, pin_y, width, height = top_left_to_visio(page_height_mm, annotation)
        box = page.DrawRectangle(pin_x - width / 2, pin_y - height / 2, pin_x + width / 2, pin_y + height / 2)
        box.Name = annotation.get("id", "annotation")
        box.Text = annotation.get("text", "")
        box.CellsU("LinePattern").FormulaU = "0"
        box.CellsU("FillPattern").FormulaU = "0"
        box.CellsU("Char.Size").FormulaU = f"{float(annotation.get('font_size_pt', style.get('font_size_pt', 9)))} pt"
        text_color = annotation.get("text_color", style.get("text_color", "#1F2937"))
        box.CellsU("Char.Color").FormulaU = f"RGB({int(text_color[1:3], 16)},{int(text_color[3:5], 16)},{int(text_color[5:7], 16)})"
        add_to_layer(page, box, annotation.get("layer"))

    output.parent.mkdir(parents=True, exist_ok=True)
    doc.SaveAs(str(output.resolve()))

    if export_png:
        export_png.parent.mkdir(parents=True, exist_ok=True)
        page.Export(str(export_png.resolve()))
    if export_pdf:
        export_pdf.parent.mkdir(parents=True, exist_ok=True)
        doc.ExportAsFixedFormat(1, str(export_pdf.resolve()), 1, 0)
    if export_svg:
        export_svg.parent.mkdir(parents=True, exist_ok=True)
        page.Export(str(export_svg.resolve()))

    doc.Close()
    try:
        visio.Quit()
    except Exception:
        pass


def main() -> int:
    parser = argparse.ArgumentParser(description="Render an editable Visio diagram from a drawing spec.")
    parser.add_argument("spec", type=Path, help="Path to drawing spec JSON.")
    parser.add_argument("--output", type=Path, default=Path("output/diagram.vsdx"), help="Output VSDX path.")
    parser.add_argument("--template", type=Path, help="Optional Visio template or existing VSDX.")
    parser.add_argument("--export-png", type=Path, help="Optional PNG preview path.")
    parser.add_argument("--export-pdf", type=Path, help="Optional PDF export path.")
    parser.add_argument("--export-svg", type=Path, help="Optional SVG export path.")
    parser.add_argument("--dry-run", action="store_true", help="Validate spec only; do not open Visio.")
    args = parser.parse_args()

    try:
        spec = load_spec(args.spec)
        validate_spec(spec)
        if args.dry_run:
            print(f"Spec valid: {args.spec}")
            return 0
        render_visio(spec, args.output, args.template, args.export_png, args.export_pdf, args.export_svg)
        print(f"Saved VSDX: {args.output}")
        return 0
    except (OSError, json.JSONDecodeError, SpecError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
