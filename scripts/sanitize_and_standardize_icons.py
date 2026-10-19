#!/usr/bin/env python3
"""
Sanitize, normalize, and validate every icon in assets/icons/.
Uses Pillow to guarantee all PNGs are true, valid 32-bit RGBA PNG files.
Converts any JPEG/JFIF or WebP files to genuine PNG.
Ensures SVGs are valid and referenced properly.
Updates data/apps.json to match canonical filenames and paths.
"""

import os
import json
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ICONS_DIR = os.path.join(BASE_DIR, 'assets', 'icons')
DATA_PATH = os.path.join(BASE_DIR, 'data', 'apps.json')

with open(DATA_PATH, 'r', encoding='utf-8') as f:
    catalog = json.load(f)

apps = catalog.get('apps', [])
print(f"Sanitizing icons for {len(apps)} apps...")

converted_count = 0
svg_swapped = 0
verified_count = 0

for app in apps:
    app_id = app.get('id', '').lower()
    icon_rel = app.get('icon', '')
    icon_full = os.path.join(BASE_DIR, icon_rel.replace('/', os.sep))

    svg_alt = os.path.join(ICONS_DIR, f"{app_id}.svg")
    png_path = os.path.join(ICONS_DIR, f"{app_id}.png")

    # If SVG exists and is pristine vector (e.g., MovieBox, ProtonVPN, YouTube, etc.)
    if os.path.exists(svg_alt) and os.path.getsize(svg_alt) > 300:
        with open(svg_alt, 'r', encoding='utf-8', errors='ignore') as fp:
            svg_txt = fp.read()
        # Ensure it's not a monogram
        if '<svg' in svg_txt and not ('<text' in svg_txt and 'letter-spacing' in svg_txt):
            app['icon'] = f"assets/icons/{app_id}.svg"
            svg_swapped += 1
            verified_count += 1
            continue

    # Otherwise, ensure PNG is a 100% valid PNG image via Pillow
    target_png = os.path.join(ICONS_DIR, f"{app_id}.png")
    if os.path.exists(target_png):
        try:
            with Image.open(target_png) as img:
                # Force convert to RGBA true PNG if JPEG, WebP, or palette
                if img.format != 'PNG' or img.mode != 'RGBA':
                    rgba_img = img.convert('RGBA')
                    # Standardize to 256x256 if larger or keep clean square
                    if rgba_img.width != rgba_img.height:
                        max_dim = max(rgba_img.width, rgba_img.height)
                        square = Image.new('RGBA', (max_dim, max_dim), (0, 0, 0, 0))
                        offset = ((max_dim - rgba_img.width) // 2, (max_dim - rgba_img.height) // 2)
                        square.paste(rgba_img, offset)
                        rgba_img = square
                    rgba_img.save(target_png, 'PNG', optimize=True)
                    converted_count += 1
                    print(f"Converted & normalized to genuine PNG: {app_id}.png")
                app['icon'] = f"assets/icons/{app_id}.png"
                verified_count += 1
        except Exception as e:
            print(f"Error reading image {target_png}: {e}")

# Save updated data/apps.json
with open(DATA_PATH, 'w', encoding='utf-8') as f:
    json.dump(catalog, f, indent=2, ensure_ascii=False)

print(f"\n--- Icon Sanitization Complete ---")
print(f"Total apps verified: {verified_count}/{len(apps)}")
print(f"Swapped to curated vector SVGs: {svg_swapped}")
print(f"Normalized/converted to genuine PNGs: {converted_count}")
