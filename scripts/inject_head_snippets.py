#!/usr/bin/env python3
"""
Inject head snippets into HTML/PHP files by inserting seo/head-snippets.html
right before the closing </head> tag.

Usage:
  python3 scripts/inject_head_snippets.py --site-root /path/to/site/root \
      [--snippet seo/head-snippets.html] [--dry-run]

Notes:
- Creates a .bak file next to each modified file.
- Skips files that already contain the yandex-verification meta or NOFACE markers.
"""
from __future__ import annotations

import argparse
from pathlib import Path

DEFAULT_SNIPPET_PATH = Path("seo/head-snippets.html")


def load_snippet(snippet_path: Path) -> str:
    if not snippet_path.exists():
        raise FileNotFoundError(f"Snippet not found: {snippet_path}")
    return snippet_path.read_text(encoding="utf-8")


def should_skip(content: str) -> bool:
    markers = [
        "yandex-verification",
        "mc.yandex.ru/metrika",
        "NOFACE.digital",
    ]
    return any(marker in content for marker in markers)


def inject_into_content(content: str, snippet: str) -> tuple[str, bool]:
    lower = content.lower()
    idx = lower.rfind("</head>")
    if idx == -1:
        return content, False
    if should_skip(content):
        return content, False
    new_content = content[:idx] + snippet + "\n" + content[idx:]
    return new_content, True


def process_file(file_path: Path, snippet: str, dry_run: bool = False) -> bool:
    try:
        text = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return False
    new_text, changed = inject_into_content(text, snippet)
    if changed and not dry_run:
        backup = file_path.with_suffix(file_path.suffix + ".bak")
        backup.write_text(text, encoding="utf-8")
        file_path.write_text(new_text, encoding="utf-8")
    return changed


def main() -> None:
    parser = argparse.ArgumentParser(description="Inject head snippets into site files")
    parser.add_argument("--site-root", required=True, help="Path to website document root")
    parser.add_argument("--snippet", default=str(DEFAULT_SNIPPET_PATH), help="Path to snippet HTML file")
    parser.add_argument("--dry-run", action="store_true", help="Do not modify files, just report")
    args = parser.parse_args()

    site_root = Path(args.site_root).resolve()
    snippet_path = Path(args.snippet).resolve()

    if not site_root.exists():
        raise FileNotFoundError(f"Site root not found: {site_root}")

    snippet = load_snippet(snippet_path)

    exts = {".html", ".htm", ".php"}
    total = 0
    changed = 0
    for path in site_root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() in exts:
            total += 1
            if process_file(path, snippet, dry_run=args.dry_run):
                changed += 1
                print(f"Injected: {path}")

    print(f"Processed {total} files. Modified {changed}.")


if __name__ == "__main__":
    main()



