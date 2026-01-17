#!/usr/bin/env python3
"""
Generate sitemap.xml from seo/urls.txt.

Usage:
  python seo/generate_sitemap.py

Reads lines in the format:
  <url> [priority] [changefreq] [lastmod]

Writes sitemap.xml to seo/sitemap.xml
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
import xml.etree.ElementTree as ET

SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
ET.register_namespace("", SITEMAP_NS)


def parse_line(line: str) -> dict:
    parts = line.strip().split()
    if not parts or parts[0].startswith("#"):
        return {}
    data = {
        "loc": parts[0],
        "priority": parts[1] if len(parts) > 1 else None,
        "changefreq": parts[2] if len(parts) > 2 else None,
        "lastmod": parts[3] if len(parts) > 3 else datetime.utcnow().strftime("%Y-%m-%d"),
    }
    return data


def generate_sitemap(url_entries: list[dict]) -> ET.ElementTree:
    urlset = ET.Element(ET.QName(SITEMAP_NS, "urlset"))
    for entry in url_entries:
        if not entry:
            continue
        url_el = ET.SubElement(urlset, ET.QName(SITEMAP_NS, "url"))
        ET.SubElement(url_el, ET.QName(SITEMAP_NS, "loc")).text = entry["loc"]
        if entry.get("lastmod"):
            ET.SubElement(url_el, ET.QName(SITEMAP_NS, "lastmod")).text = entry["lastmod"]
        if entry.get("changefreq"):
            ET.SubElement(url_el, ET.QName(SITEMAP_NS, "changefreq")).text = entry["changefreq"]
        if entry.get("priority"):
            ET.SubElement(url_el, ET.QName(SITEMAP_NS, "priority")).text = entry["priority"]
    return ET.ElementTree(urlset)


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    seo_dir = project_root / "seo"
    urls_file = seo_dir / "urls.txt"
    sitemap_file = seo_dir / "sitemap.xml"

    if not urls_file.exists():
        raise FileNotFoundError(f"URLs file not found: {urls_file}")

    url_entries: list[dict] = []
    with urls_file.open("r", encoding="utf-8") as f:
        for raw in f:
            data = parse_line(raw)
            if data:
                url_entries.append(data)

    tree = generate_sitemap(url_entries)
    tree.write(sitemap_file, encoding="utf-8", xml_declaration=True)
    print(f"Generated sitemap with {len(url_entries)} URLs at {sitemap_file}")


if __name__ == "__main__":
    main()



