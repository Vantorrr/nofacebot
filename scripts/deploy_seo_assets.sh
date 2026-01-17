#!/bin/bash
set -euo pipefail

# Copy SEO assets to site root
# Usage: ./scripts/deploy_seo_assets.sh /var/www/site

if [ $# -lt 1 ]; then
  echo "Usage: $0 /path/to/site/root"
  exit 1
fi

SITE_ROOT="$1"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

mkdir -p "$SITE_ROOT"

# robots.txt
if [ -f "$PROJECT_ROOT/seo/robots.txt" ]; then
  cp "$PROJECT_ROOT/seo/robots.txt" "$SITE_ROOT/robots.txt"
  echo "Copied robots.txt"
fi

# sitemap.xml
if [ -f "$PROJECT_ROOT/seo/sitemap.xml" ]; then
  cp "$PROJECT_ROOT/seo/sitemap.xml" "$SITE_ROOT/sitemap.xml"
  echo "Copied sitemap.xml"
fi

# Yandex verification (optional)
if [ -f "$PROJECT_ROOT/seo/verify/yandex_7ec05ab6f0366a7e.html" ]; then
  cp "$PROJECT_ROOT/seo/verify/yandex_7ec05ab6f0366a7e.html" "$SITE_ROOT/yandex_7ec05ab6f0366a7e.html"
  echo "Copied Yandex verification file"
fi

echo "SEO assets deployed to $SITE_ROOT"



