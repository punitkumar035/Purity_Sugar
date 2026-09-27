"""
audit_stencils.py
Audits the current stencils and property behaviors against Sugar's Help Book.
"""

import os
import re
from pathlib import Path

HELPBOOK_ROOT = Path(".agents/skills/sugars-helpbook/references")
HTML_PATH = Path("massecuite_phase4_8_9_1_centrifugal_solver.html")
PYTHON_STATIONS_DIR = Path("solver/stations")
DOCS_STENCIL_DIR = Path("docs/stencil/modules")
DOCS_PW_DIR = Path("docs/property-windows/modules")

print("=== 1. HELPBOOK EQUIPMENT & STATION REFERENCE CHAPTERS ===")
helpbook_equipment = sorted([d.name for d in HELPBOOK_ROOT.iterdir() if d.is_dir()])
print(f"Total Helpbook station chapters: {len(helpbook_equipment)}")
for eq in helpbook_equipment:
    files = list((HELPBOOK_ROOT / eq).glob("*.md"))
    print(f"  - {eq}: {[f.stem for f in files]}")

print("\n=== 2. PYTHON SOLVER STATIONS ===")
py_stations = sorted([f.stem for f in PYTHON_STATIONS_DIR.glob("*.py") if f.stem not in ("__init__", "base")])
print(f"Total Python solver stations: {len(py_stations)}: {py_stations}")

print("\n=== 3. WEB APP (HTML) NODE DEFINITIONS & PROPERTY WINDOWS ===")
with open(HTML_PATH, "r", encoding="utf-8") as f:
    html_content = f.read()

# Find nodeDefs
node_defs_match = re.search(r"const nodeDefs = \{(.*?)\n  \};", html_content, re.DOTALL)
if node_defs_match:
    node_defs_text = node_defs_match.group(1)
    nodes = re.findall(r"^\s*([a-zA-Z0-9_]+)\s*:\s*\{", node_defs_text, re.MULTILINE)
    print(f"HTML nodeDefs ({len(nodes)}): {nodes}")

# Find palette items in HTML
palette_matches = re.findall(r'class="[^"]*tool-btn[^"]*"[^>]*data-type="([^"]+)"', html_content)
if not palette_matches:
    palette_matches = re.findall(r'data-type="([^"]+)"', html_content)
print(f"HTML palette items ({len(palette_matches)}): {palette_matches}")

# Check property window renderers in HTML
prop_dialog_funcs = re.findall(r"function render([A-Za-z0-9_]+)(?:Dialog|Pane|Props|Workspace)", html_content)
print(f"Property dialog render functions: {prop_dialog_funcs}")

# Check openPropertyWindow routing
open_props_idx = html_content.find("function openPropertyWindow")
if open_props_idx != -1:
    print("\nopenPropertyWindow routing snippet:")
    print(html_content[open_props_idx:open_props_idx+1200])

print("\n=== 4. DOCS STENCIL MODULES ===")
stencils = sorted([f.name for f in DOCS_STENCIL_DIR.glob("*.md")])
print(f"Docs stencil files ({len(stencils)}): {stencils}")

print("\n=== 5. DOCS PROPERTY WINDOW MODULES ===")
pws = sorted([f.name for f in DOCS_PW_DIR.glob("*.md")])
print(f"Docs property window files ({len(pws)}): {pws}")
