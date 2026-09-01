#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def split_blocks(text: str) -> list[str]:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return [block.strip() for block in re.split(r"\n\s*\n", text) if block.strip()]


def find_images(article_dir: Path) -> list[Path]:
    image_dir = article_dir / "images"
    if not image_dir.exists():
        return []
    return sorted(
        [
            path
            for path in image_dir.iterdir()
            if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
        ]
    )


def img_src(article: Path, out: Path, src: str) -> str:
    candidate = (article.parent / src).resolve()
    if candidate.exists():
        return candidate.as_uri()
    return src


def render(article: Path, out: Path) -> None:
    source = article.read_text(encoding="utf-8-sig", errors="ignore")
    blocks = split_blocks(source)
    images = find_images(article.parent)
    has_markdown_images = bool(re.search(r"!\[[^\]]*\]\([^)]+\)", source))
    image_idx = 0
    used_first_figure = False
    body: list[str] = []
    title = article.parent.name

    i = 0
    while i < len(blocks):
        block = blocks[i]
        lines = block.splitlines()
        first = lines[0].strip()
        if first.startswith("# "):
            title = first[2:].strip()
            body.append(f"<h1>{esc(title)}</h1>")
            i += 1
            continue
        if first == "---":
            i += 1
            continue
        image_match = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", first)
        if image_match:
            alt, src = image_match.groups()
            caption = alt
            if i + 1 < len(blocks):
                next_block = blocks[i + 1].strip()
                if (
                    next_block
                    and not next_block.startswith("#")
                    and not next_block.startswith("!")
                    and not next_block.startswith("- ")
                    and not next_block.startswith(">")
                    and len(next_block) <= 140
                ):
                    caption = " ".join(line.strip() for line in next_block.splitlines())
                    i += 1
            body.append(
                "<figure>"
                f"<img src=\"{esc(img_src(article, out, src))}\" alt=\"{esc(alt)}\">"
                f"<figcaption>{esc(caption)}</figcaption>"
                "</figure>"
            )
            i += 1
            continue
        if all(line.startswith("- ") for line in lines):
            items = []
            for line in lines:
                item = re.sub(r"\*\*(.*?)\*\*", r"\1", line[2:].strip())
                items.append(f"<span>{esc(item)}</span>")
            body.append(f"<div class=\"meta\">{' · '.join(items)}</div>")
            i += 1
            continue
        if all(line.startswith(">") for line in lines):
            for line in lines:
                quote = line.lstrip("> ").strip()
                if quote:
                    body.append(f"<blockquote>{esc(quote)}</blockquote>")
            i += 1
            continue

        text = " ".join(line.strip() for line in lines if line.strip())
        if not text:
            i += 1
            continue
        if len(text) <= 34 and not text.endswith(("。", "！", "？", "；", ".", "!", "?")):
            body.append(f"<h2>{esc(text)}</h2>")
            i += 1
            continue

        cls = "intro" if not used_first_figure and len(body) > 3 else ""
        body.append(f"<p class=\"{cls}\">{esc(text)}</p>")

        if images and image_idx < len(images):
            # Place the first image after the opening setup, then subsequent images
            # after later paragraphs. Existing article captions remain in the text.
            should_place = (
                (not used_first_figure and len("".join(body)) > 900)
                or (used_first_figure and len(body) % 10 == 0)
            )
            if should_place and not has_markdown_images:
                img = images[image_idx]
                rel = img.relative_to(out.parent).as_posix() if img.is_relative_to(out.parent) else img.resolve().as_uri()
                body.append(
                    "<figure>"
                    f"<img src=\"{esc(rel)}\" alt=\"{esc(img.stem)}\">"
                    f"<figcaption>{esc(img.stem)}</figcaption>"
                    "</figure>"
                )
                image_idx += 1
                used_first_figure = True
        i += 1

    while images and image_idx < len(images) and not has_markdown_images:
        img = images[image_idx]
        rel = img.resolve().as_uri()
        body.append(
            "<figure>"
            f"<img src=\"{esc(rel)}\" alt=\"{esc(img.stem)}\">"
            f"<figcaption>{esc(img.stem)}</figcaption>"
            "</figure>"
        )
        image_idx += 1

    html_doc = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <style>
    :root {{
      --ink: #252525;
      --muted: #777;
      --line: #ece6d8;
      --accent: #f3c63f;
      --accent-2: #0f766e;
      --paper: #fffdf8;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: #f7f7f4;
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
      line-height: 1.85;
      letter-spacing: 0;
    }}
    main {{
      width: 900px;
      margin: 0 auto;
      background: var(--paper);
      padding: 38px 78px 54px;
    }}
    .kicker {{
      font-size: 14px;
      color: var(--accent-2);
      font-weight: 700;
      margin-bottom: 10px;
    }}
    h1 {{
      font-size: 28px;
      line-height: 1.36;
      margin: 0 0 10px;
      font-weight: 800;
    }}
    .meta {{
      color: var(--muted);
      font-size: 13px;
      border-bottom: 1px solid var(--line);
      padding-bottom: 22px;
      margin-bottom: 26px;
    }}
    .intro {{
      background: linear-gradient(180deg, #fff9df, #fffdf8);
      border-top: 5px solid var(--accent);
      padding: 18px 22px;
      margin: 24px 0;
    }}
    blockquote {{
      margin: 18px 0;
      padding: 8px 0 8px 18px;
      border-left: 4px solid var(--accent);
      color: #444;
      font-size: 16px;
      font-weight: 600;
    }}
    h2 {{
      display: table;
      margin: 34px auto 18px;
      padding: 2px 8px;
      background: var(--accent);
      font-size: 21px;
      line-height: 1.45;
      font-weight: 850;
      text-align: center;
    }}
    p {{
      font-size: 16px;
      margin: 13px 0;
    }}
    figure {{
      margin: 24px 0 26px;
    }}
    img {{
      display: block;
      width: 100%;
      height: auto;
      border-radius: 3px;
    }}
    figcaption {{
      margin-top: 9px;
      color: #676767;
      font-size: 13px;
      line-height: 1.65;
    }}
  </style>
</head>
<body>
  <main>
    <div class="kicker">播客类型图文版</div>
    {"".join(body)}
  </main>
</body>
</html>
"""
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html_doc, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("article", type=Path)
    parser.add_argument("out", type=Path)
    args = parser.parse_args()
    render(args.article, args.out)


if __name__ == "__main__":
    main()
