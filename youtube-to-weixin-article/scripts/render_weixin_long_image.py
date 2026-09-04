#!/usr/bin/env python3
"""Render a simple WeChat-style Markdown article to a vertical PNG."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


IMAGE_RE = re.compile(r"!\[(.*?)\]\((.*?)\)")
TOKEN_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9'._:/%$+-]*|.", re.S)


def find_font(preferred_size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = []
    if sys.platform.startswith("win"):
        base = Path("C:/Windows/Fonts")
        candidates = [
            base / ("msyhbd.ttc" if bold else "msyh.ttc"),
            base / ("simheibd.ttf" if bold else "simhei.ttf"),
            base / "simsun.ttc",
        ]
    elif sys.platform == "darwin":
        candidates = [
            Path("/System/Library/Fonts/PingFang.ttc"),
            Path("/System/Library/Fonts/STHeiti Light.ttc"),
        ]
    else:
        candidates = [
            Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
            Path("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"),
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        ]

    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), preferred_size)
    return ImageFont.load_default()


def text_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> float:
    return draw.textlength(text, font=font)


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int) -> list[str]:
    lines: list[str] = []
    current = ""
    for token in TOKEN_RE.findall(text.strip()):
        trial = current + token
        if current and text_width(draw, trial, font) > max_width:
            lines.append(current)
            if text_width(draw, token, font) > max_width:
                broken = wrap_text(draw, token[1:], font, max_width)
                current = token[0]
                for part in broken:
                    trial = current + part
                    if text_width(draw, trial, font) > max_width:
                        lines.append(current)
                        current = part
                    else:
                        current = trial
            else:
                current = token
        else:
            current = trial
    if current:
        lines.append(current)
    return lines or [""]


def resolve_image(path_text: str, md_path: Path, assets_dir: Path | None) -> Path:
    path_text = path_text.strip().strip('"').strip("'")
    candidate = Path(path_text)
    if candidate.is_absolute():
        return candidate
    if assets_dir:
        in_assets = assets_dir / candidate
        if in_assets.exists():
            return in_assets
        by_name = assets_dir / candidate.name
        if by_name.exists():
            return by_name
    return md_path.parent / candidate


def parse_blocks(markdown: str) -> list[tuple[str, str, str | None]]:
    blocks: list[tuple[str, str, str | None]] = []
    paragraph: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            blocks.append(("p", " ".join(x.strip() for x in paragraph), None))
            paragraph = []

    for raw_line in markdown.splitlines():
        line = raw_line.strip()
        if not line:
            flush_paragraph()
            continue

        image_match = IMAGE_RE.search(line)
        if image_match:
            flush_paragraph()
            blocks.append(("image", image_match.group(2), image_match.group(1)))
            continue

        if line.startswith("# "):
            flush_paragraph()
            blocks.append(("h1", line[2:].strip(), None))
        elif line.startswith("## "):
            flush_paragraph()
            blocks.append(("h2", line[3:].strip(), None))
        elif line.startswith(">"):
            flush_paragraph()
            blocks.append(("quote", line.lstrip("> ").strip(), None))
        elif (line.startswith('"') and line.endswith('"')) or (line.startswith("“") and line.endswith("”")):
            flush_paragraph()
            blocks.append(("quote", line.strip('"“”'), None))
        else:
            paragraph.append(line)

    flush_paragraph()
    return blocks


class Renderer:
    def __init__(self, width: int, padding: int, bg: str) -> None:
        self.width = width
        self.padding = padding
        self.content_width = width - padding * 2
        self.bg = bg
        scale = width / 1200
        self.title = find_font(max(38, int(52 * scale)), bold=True)
        self.h2 = find_font(max(28, int(36 * scale)), bold=True)
        self.body = find_font(max(25, int(30 * scale)))
        self.quote = find_font(max(27, int(34 * scale)))
        self.caption = find_font(max(20, int(23 * scale)))
        self.footer = find_font(max(18, int(20 * scale)))
        self.measure = ImageDraw.Draw(Image.new("RGB", (width, 10), bg))

    def paragraph_height(self, text: str, font: ImageFont.ImageFont, spacing: int, max_width: int | None = None) -> tuple[list[str], int]:
        available_width = max_width or self.content_width
        lines = wrap_text(self.measure, text, font, available_width)
        bbox = self.measure.textbbox((0, 0), "国", font=font)
        line_h = bbox[3] - bbox[1] + spacing
        return lines, len(lines) * line_h

    def estimate_height(self, blocks: list[tuple[str, str, str | None]], md_path: Path, assets_dir: Path | None) -> int:
        h = 90
        for kind, text, alt in blocks:
            if kind == "h1":
                _, ph = self.paragraph_height(text, self.title, 14)
                h += ph + 42
            elif kind == "h2":
                _, ph = self.paragraph_height(text, self.h2, 12, self.content_width - 24)
                h += ph + 34
            elif kind == "quote":
                _, ph = self.paragraph_height(text, self.quote, 12, self.content_width - 56)
                h += ph + 48
            elif kind == "image":
                img_path = resolve_image(text, md_path, assets_dir)
                if img_path.exists():
                    with Image.open(img_path) as im:
                        ratio = self.content_width / im.width
                        h += int(im.height * ratio) + 52
                else:
                    h += 120
                if alt:
                    _, ch = self.paragraph_height(alt, self.caption, 8)
                    h += ch
            else:
                _, ph = self.paragraph_height(text, self.body, 11)
                h += ph + 22
        return h + 90

    def draw_wrapped(self, draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, font: ImageFont.ImageFont, fill: str, spacing: int, max_width: int | None = None) -> int:
        x, y = xy
        available_width = max_width or self.content_width
        lines = wrap_text(draw, text, font, available_width)
        bbox = draw.textbbox((0, 0), "国", font=font)
        line_h = bbox[3] - bbox[1] + spacing
        for line in lines:
            draw.text((x, y), line, font=font, fill=fill)
            y += line_h
        return y

    def render(self, blocks: list[tuple[str, str, str | None]], md_path: Path, assets_dir: Path | None, output: Path) -> None:
        height = self.estimate_height(blocks, md_path, assets_dir)
        canvas = Image.new("RGB", (self.width, height), self.bg)
        draw = ImageDraw.Draw(canvas)
        y = 70

        for kind, text, alt in blocks:
            x = self.padding
            if kind == "h1":
                y = self.draw_wrapped(draw, (x, y), text, self.title, "#111111", 14) + 42
            elif kind == "h2":
                draw.rounded_rectangle((x, y + 8, x + 8, y + 44), radius=4, fill="#222222")
                y = self.draw_wrapped(draw, (x + 24, y), text, self.h2, "#111111", 12, self.content_width - 24) + 28
            elif kind == "quote":
                inner_pad = 28
                inner_width = self.content_width - inner_pad * 2
                lines, ph = self.paragraph_height(text, self.quote, 12, inner_width)
                box = (x, y, x + self.content_width, y + ph + 34)
                draw.rounded_rectangle(box, radius=14, fill="#f4f1ea")
                qy = y + 17
                line_h = max(42, self.quote.size + 12) if hasattr(self.quote, "size") else 44
                for line in lines:
                    draw.text((x + inner_pad, qy), line, font=self.quote, fill="#333333")
                    qy += line_h
                y = box[3] + 24
            elif kind == "image":
                img_path = resolve_image(text, md_path, assets_dir)
                if img_path.exists():
                    with Image.open(img_path) as im:
                        im = im.convert("RGB")
                        ratio = self.content_width / im.width
                        resized = im.resize((self.content_width, int(im.height * ratio)))
                    canvas.paste(resized, (x, y))
                    y += resized.height + 14
                else:
                    draw.rounded_rectangle((x, y, x + self.content_width, y + 92), radius=10, outline="#dddddd", width=2)
                    self.draw_wrapped(draw, (x + 20, y + 24), f"Missing image: {text}", self.caption, "#9a3b30", 8, self.content_width - 40)
                    y += 112
                if alt:
                    y = self.draw_wrapped(draw, (x, y), alt, self.caption, "#777777", 8) + 28
            else:
                y = self.draw_wrapped(draw, (x, y), text, self.body, "#222222", 11) + 22

        output.parent.mkdir(parents=True, exist_ok=True)
        canvas.crop((0, 0, self.width, min(y + 60, height))).save(output, quality=95)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a WeChat-style long PNG from a Markdown article.")
    parser.add_argument("markdown", type=Path, help="Markdown article path")
    parser.add_argument("-o", "--output", type=Path, help="Output PNG path")
    parser.add_argument("--assets-dir", type=Path, help="Directory for local images")
    parser.add_argument("--width", type=int, default=1200, help="Canvas width, default 1200")
    parser.add_argument("--padding", type=int, default=96, help="Side padding, default 96")
    parser.add_argument("--background", default="#fffdf8", help="Background color")
    args = parser.parse_args()

    md_path = args.markdown
    output = args.output or md_path.with_suffix(".long.png")
    markdown = md_path.read_text(encoding="utf-8")
    blocks = parse_blocks(markdown)
    Renderer(args.width, args.padding, args.background).render(blocks, md_path, args.assets_dir, output)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
