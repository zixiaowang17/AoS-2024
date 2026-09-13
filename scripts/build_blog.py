#!/usr/bin/env python3
"""Render docs/blog-post.md using the saved website layout. Requires Pandoc."""
import html
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    source = (ROOT / "docs/blog-post.md").read_text()
    title = re.search(r"^# (.+)$", source, re.MULTILINE)
    if not title:
        raise SystemExit("Start the Markdown with a title: # Your title")
    body = subprocess.run(
        ["pandoc", "--from=gfm", "--to=html5"], input=source,
        capture_output=True, text=True, check=True,
    ).stdout
    template = (ROOT / "assets/blog-template.html").read_text()
    page = template.replace("{{title}}", html.escape(title.group(1))).replace("{{body}}", body)
    (ROOT / "docs/blog-post.html").write_text(page)
    print("Built docs/blog-post.html")


if __name__ == "__main__":
    main()
