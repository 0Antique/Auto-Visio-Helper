# Visio Automation

Use Windows COM automation when Microsoft Visio is installed locally. Prefer scripted creation over GUI clicking.

## Preferred Path

1. Write or update a JSON drawing spec.
2. Dry-run validate it:

   ```powershell
   python scripts/render_visio.py spec.json --dry-run
   ```

3. Render it:

   ```powershell
   python scripts/render_visio.py spec.json --output output\figure.vsdx --export-png output\figure.png
   ```

4. Inspect the exported preview.
5. Revise the spec and rerun if needed.

## Requirements

- Windows.
- Microsoft Visio installed.
- Python with `pywin32` for COM automation:

  ```powershell
  python -m pip install pywin32
  ```

If Visio or `pywin32` is unavailable, stop after producing the drawing spec and explain what remains to render locally.

## Template Usage

Use `--template path\to\template.vsdx` when an existing Visio file should provide page setup, styles, stencils, or base content.

Do not read binary `.vsdx` files into context. Treat them as assets and pass paths to scripts.

## Editable Output Rules

- Create Visio primitives: shapes, connectors, text boxes, and layers.
- Name shapes with stable IDs from the drawing spec.
- Do not use a pasted bitmap as the final figure.
- Preserve grouping intent through layers and names even when full Visio group containers are not used.

## Troubleshooting

- COM error opening Visio: verify Visio desktop is installed and licensed.
- `No module named win32com`: install `pywin32`.
- Export failure: save the VSDX first, then retry export.
- Text clipped: increase node width/height or shorten labels in the spec.
- Wrong arrow direction: check `from` and `to` node IDs in `edges`.
