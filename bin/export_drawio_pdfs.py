#!/usr/bin/env python3
"""Export simple uncompressed draw.io diagrams to printable PDFs.

This renderer intentionally supports the small subset used by this repo:
rectangles, swimlanes, ellipses, process boxes, straight connectors, labels,
basic fills and strokes. It avoids requiring the draw.io desktop app in local
build environments.
"""

from __future__ import annotations

import html
import math
import re
import textwrap
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "docs" / "systeme-info-si" / "drawio"
OUTPUT_DIR = ROOT / "docs" / "systeme-info-si" / "pdf"

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SCALE = 2
MARGIN = 40


@dataclass
class Cell:
    id: str
    value: str
    style: dict[str, str]
    parent: str | None
    vertex: bool
    edge: bool
    source: str | None
    target: str | None
    x: float = 0
    y: float = 0
    w: float = 0
    h: float = 0


def parse_style(style: str | None) -> dict[str, str]:
    result: dict[str, str] = {}
    for part in (style or "").split(";"):
        if not part:
            continue
        if "=" in part:
            key, value = part.split("=", 1)
            result[key] = value
        else:
            result[part] = "1"
    return result


def clean_label(value: str | None) -> str:
    text = html.unescape(value or "")
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
    text = re.sub(r"<[^>]+>", "", text)
    return text.replace("&nbsp;", " ").strip()


def color(value: str | None, fallback: str) -> str:
    if not value or value == "none":
        return fallback
    return value


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    path = BOLD_FONT if bold else FONT
    return ImageFont.truetype(path, size * SCALE)


def scaled_box(cell: Cell) -> tuple[int, int, int, int]:
    x1 = int((cell.x + MARGIN) * SCALE)
    y1 = int((cell.y + MARGIN) * SCALE)
    x2 = int((cell.x + cell.w + MARGIN) * SCALE)
    y2 = int((cell.y + cell.h + MARGIN) * SCALE)
    return x1, y1, x2, y2


def center(cell: Cell) -> tuple[int, int]:
    return (
        int((cell.x + cell.w / 2 + MARGIN) * SCALE),
        int((cell.y + cell.h / 2 + MARGIN) * SCALE),
    )


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font_obj: ImageFont.FreeTypeFont, width: int) -> list[str]:
    lines: list[str] = []
    for raw_line in text.splitlines() or [""]:
        words = raw_line.split()
        if not words:
            lines.append("")
            continue
        line = words[0]
        for word in words[1:]:
            candidate = f"{line} {word}"
            if draw.textbbox((0, 0), candidate, font=font_obj)[2] <= width:
                line = candidate
            else:
                lines.append(line)
                line = word
        lines.append(line)
    return lines


def draw_text_centered(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], text: str, size: int, bold: bool) -> None:
    if not text:
        return
    x1, y1, x2, y2 = box
    font_obj = font(size, bold)
    width = max(20, x2 - x1 - 16 * SCALE)
    lines = wrap_text(draw, text, font_obj, width)
    metrics = [draw.textbbox((0, 0), line, font=font_obj) for line in lines]
    line_h = max((m[3] - m[1] for m in metrics), default=size * SCALE) + 3 * SCALE
    total_h = line_h * len(lines)
    y = y1 + max(0, (y2 - y1 - total_h) // 2)
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font_obj)
        x = x1 + max(0, (x2 - x1 - (bbox[2] - bbox[0])) // 2)
        draw.text((x, y), line, fill="#111827", font=font_obj)
        y += line_h


def draw_arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], stroke: str, width: int, dashed: bool) -> None:
    sx, sy = start
    ex, ey = end
    width *= SCALE
    if dashed:
        segments = 18
        for i in range(segments):
            if i % 2 == 0:
                a = i / segments
                b = (i + 1) / segments
                draw.line((sx + (ex - sx) * a, sy + (ey - sy) * a, sx + (ex - sx) * b, sy + (ey - sy) * b), fill=stroke, width=width)
    else:
        draw.line((sx, sy, ex, ey), fill=stroke, width=width)

    angle = math.atan2(ey - sy, ex - sx)
    arrow_len = 12 * SCALE
    arrow_w = 7 * SCALE
    p1 = (ex, ey)
    p2 = (ex - arrow_len * math.cos(angle) + arrow_w * math.sin(angle), ey - arrow_len * math.sin(angle) - arrow_w * math.cos(angle))
    p3 = (ex - arrow_len * math.cos(angle) - arrow_w * math.sin(angle), ey - arrow_len * math.sin(angle) + arrow_w * math.cos(angle))
    draw.polygon((p1, p2, p3), fill=stroke)


def parse_file(path: Path) -> tuple[int, int, list[Cell]]:
    tree = ET.parse(path)
    model = tree.find(".//mxGraphModel")
    page_w = int(float(model.attrib.get("pageWidth", "1169"))) if model is not None else 1169
    page_h = int(float(model.attrib.get("pageHeight", "827"))) if model is not None else 827

    cells: list[Cell] = []
    for node in tree.findall(".//mxCell"):
        geometry = node.find("mxGeometry")
        cell = Cell(
            id=node.attrib.get("id", ""),
            value=clean_label(node.attrib.get("value")),
            style=parse_style(node.attrib.get("style")),
            parent=node.attrib.get("parent"),
            vertex=node.attrib.get("vertex") == "1",
            edge=node.attrib.get("edge") == "1",
            source=node.attrib.get("source"),
            target=node.attrib.get("target"),
        )
        if geometry is not None:
            cell.x = float(geometry.attrib.get("x", "0"))
            cell.y = float(geometry.attrib.get("y", "0"))
            cell.w = float(geometry.attrib.get("width", "0"))
            cell.h = float(geometry.attrib.get("height", "0"))
        cells.append(cell)
    return page_w, page_h, cells


def draw_vertex(draw: ImageDraw.ImageDraw, cell: Cell) -> None:
    box = scaled_box(cell)
    style = cell.style
    fill = color(style.get("fillColor"), "#ffffff")
    stroke = color(style.get("strokeColor"), "#64748b")
    width = int(float(style.get("strokeWidth", "1"))) * SCALE
    is_bold = style.get("fontStyle") == "1"
    font_size = int(float(style.get("fontSize", "12")))

    if "ellipse" in style.get("shape", ""):
        draw.ellipse(box, fill=fill, outline=stroke, width=width)
    else:
        radius = 10 * SCALE if style.get("rounded") == "1" else 0
        draw.rounded_rectangle(box, radius=radius, fill=fill, outline=stroke, width=width)

    if "swimlane" in style:
        x1, y1, x2, _ = box
        header_h = 30 * SCALE
        draw.rectangle((x1, y1, x2, y1 + header_h), fill=fill, outline=stroke, width=width)
        draw_text_centered(draw, (x1, y1, x2, y1 + header_h), cell.value, font_size, True)
    else:
        draw_text_centered(draw, box, cell.value, font_size, is_bold)


def export_one(path: Path) -> Path:
    page_w, page_h, cells = parse_file(path)
    image = Image.new("RGB", ((page_w + MARGIN * 2) * SCALE, (page_h + MARGIN * 2) * SCALE), "white")
    draw = ImageDraw.Draw(image)

    by_id = {cell.id: cell for cell in cells}
    swimlanes = [cell for cell in cells if cell.vertex and "swimlane" in cell.style]
    vertices = [cell for cell in cells if cell.vertex and "swimlane" not in cell.style and cell.w and cell.h]
    edges = [cell for cell in cells if cell.edge]

    for cell in swimlanes:
        draw_vertex(draw, cell)

    for cell in edges:
        if not cell.source or not cell.target or cell.source not in by_id or cell.target not in by_id:
            continue
        source = by_id[cell.source]
        target = by_id[cell.target]
        stroke = color(cell.style.get("strokeColor"), "#64748b")
        width = int(float(cell.style.get("strokeWidth", "1")))
        draw_arrow(draw, center(source), center(target), stroke, width, cell.style.get("dashed") == "1")
        if cell.value:
            sx, sy = center(source)
            tx, ty = center(target)
            label_font = font(int(float(cell.style.get("fontSize", "11"))), False)
            label = "\n".join(textwrap.wrap(cell.value, width=24))
            bbox = draw.multiline_textbbox((0, 0), label, font=label_font, spacing=2 * SCALE)
            lx = (sx + tx) // 2 - (bbox[2] - bbox[0]) // 2
            ly = (sy + ty) // 2 - (bbox[3] - bbox[1]) // 2
            pad = 3 * SCALE
            draw.rounded_rectangle((lx - pad, ly - pad, lx + bbox[2] - bbox[0] + pad, ly + bbox[3] - bbox[1] + pad), radius=4 * SCALE, fill="white")
            draw.multiline_text((lx, ly), label, fill="#111827", font=label_font, spacing=2 * SCALE, align="center")

    for cell in vertices:
        draw_vertex(draw, cell)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output = OUTPUT_DIR / f"{path.stem}.pdf"
    image.save(output, "PDF", resolution=150.0)
    return output


def main() -> None:
    outputs = [export_one(path) for path in sorted(SOURCE_DIR.glob("*.drawio"))]
    for output in outputs:
        print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
