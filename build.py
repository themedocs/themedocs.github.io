#!/usr/bin/env python3
"""
Documentation home — the chooser page that points at each theme's docs repo.

    python3 build.py     themes.toml + index.md -> docs/

Each theme's documentation is its own repository, published at /<slug>/. This
site is only the front door, so it is a single page plus a 404.
"""

import html
import re
import shutil
import tomllib
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "docs"
STYLE = ROOT / "style.css"
BASE = "https://themedocs.github.io"


def load_toml(path):
    with open(path, "rb") as fh:
        return tomllib.load(fh)


def split_front_matter(text):
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    meta = {}
    for line in text[3:end].splitlines():
        key, _, value = line.partition(":")
        if key.strip():
            meta[key.strip()] = value.strip().strip("\"'")
    return meta, text[end + 4 :].lstrip("\n")


def shell(*, title, description, url, body, css):
    head = [
        "<!doctype html><html lang=en><head><meta charset=utf-8>",
        '<meta name=viewport content="width=device-width,initial-scale=1">',
        f"<title>{html.escape(title)}</title>",
    ]
    if description:
        head.append(f'<meta name=description content="{html.escape(description)}">')
    head += [
        f'<link rel=canonical href="{BASE}{url}">',
        f'<meta property="og:title" content="{html.escape(title)}">',
        f'<meta property="og:url" content="{BASE}{url}">',
        '<meta property="og:type" content="website">',
        '<meta name="twitter:card" content="summary">',
        f"<style>:root{{--a:#c2410c}}{css}</style>",
    ]
    return (
        "".join(head)
        + "</head><body>"
        + '<a class=skip href="#main">Skip to content</a>'
        + '<div class="wrap wide"><main id=main>'
        + body
        + "</main></div>"
        + "</body></html>"
    )


def build():
    css = re.sub(r"\s+", " ", re.sub(r"/\*.*?\*/", "", STYLE.read_text(), flags=re.S)).strip()
    css = re.sub(r"\s*([{}:;,>])\s*", r"\1", css).replace(";}", "}")

    themes = load_toml(ROOT / "themes.toml")["theme"]
    meta, raw = split_front_matter((ROOT / "index.md").read_text(encoding="utf-8"))
    intro = markdown.markdown(raw, extensions=["extra", "smarty"])

    picks = "".join(
        f'<a class=pick href="/{t["slug"]}/"><b>{html.escape(t["name"])}</b>'
        f'<span>{html.escape(t.get("tagline", ""))}</span></a>'
        for t in themes
    )

    BUILD.mkdir(parents=True, exist_ok=True)
    for item in BUILD.iterdir():
        shutil.rmtree(item) if item.is_dir() else item.unlink()

    (BUILD / "index.html").write_text(
        shell(
            title=meta.get("title") or "Theme documentation",
            description=meta.get("description", ""),
            url="/",
            body=f'<h1>{html.escape(meta.get("title") or "Theme documentation")}</h1>'
                 f"{intro}<div class=picks>{picks}</div>",
            css=css,
        ),
        encoding="utf-8",
    )
    (BUILD / "404.html").write_text(
        shell(
            title="Page not found",
            description="",
            url="/",
            body="<h1>Page not found</h1><p>That page has moved or never existed. "
                 '<a href="/">Start from the documentation home</a>.</p>',
            css=css,
        ),
        encoding="utf-8",
    )
    (BUILD / ".nojekyll").write_text("")

    # Each theme repo publishes its own sitemap; this one lists where they are.
    (BUILD / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\n"
        + "".join(f"Sitemap: {BASE}/{t['slug']}/sitemap.xml\n" for t in themes)
    )
    print(f"  1 page + 404 · {len(themes)} themes linked")


if __name__ == "__main__":
    build()
