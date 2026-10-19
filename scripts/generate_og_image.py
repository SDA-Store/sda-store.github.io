#!/usr/bin/env python3
"""
Generate a 1200x630 Open Graph Social Preview Image for SDA Store.
Used by Google, Twitter Cards, Discord, Telegram, WhatsApp, and Facebook.
"""

import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(BASE_DIR, 'assets', 'og-image.png')

WIDTH, HEIGHT = 1200, 630

def create_og_image():
    # 1. Base Dark Canvas
    img = Image.new('RGBA', (WIDTH, HEIGHT), '#09090b')
    draw = ImageDraw.Draw(img)

    # 2. Draw subtle geometric background grid (24px)
    grid_color = (255, 255, 255, 8)
    for x in range(0, WIDTH, 32):
        draw.line([(x, 0), (x, HEIGHT)], fill=grid_color, width=1)
    for y in range(0, HEIGHT, 32):
        draw.line([(0, y), (WIDTH, y)], fill=grid_color, width=1)

    # 3. Top accent gradient bar (Emerald to white)
    accent_bar_height = 6
    for x in range(WIDTH):
        t = x / WIDTH
        # Interpolate from #10b981 (16, 185, 129) to #fafafa (250, 250, 250)
        r = int(16 * (1 - t) + 250 * t)
        g = int(185 * (1 - t) + 250 * t)
        b = int(129 * (1 - t) + 250 * t)
        draw.line([(x, 0), (x, accent_bar_height)], fill=(r, g, b, 255))

    # 4. Brand stamp circle on top left
    # Draw dark container card
    card_margin_x = 80
    card_margin_y = 65
    draw.rounded_rectangle(
        [(card_margin_x, card_margin_y), (WIDTH - card_margin_x, HEIGHT - card_margin_y)],
        radius=28,
        fill=(18, 18, 21, 230),
        outline=(39, 39, 42, 255),
        width=2
    )

    # Brand pill top
    draw.rounded_rectangle(
        [(card_margin_x + 50, card_margin_y + 45), (card_margin_x + 230, card_margin_y + 85)],
        radius=20,
        fill=(24, 24, 27, 255),
        outline=(63, 63, 70, 255),
        width=1
    )
    # Emerald dot
    draw.ellipse(
        [(card_margin_x + 65, card_margin_y + 59), (card_margin_x + 77, card_margin_y + 71)],
        fill=(16, 185, 129, 255)
    )

    try:
        font_logo = ImageFont.truetype("arialbd.ttf", 15)
        font_title = ImageFont.truetype("arialbd.ttf", 54)
        font_serif = ImageFont.truetype("georgia.ttf", 50)
        font_sub = ImageFont.truetype("arial.ttf", 22)
        font_badge = ImageFont.truetype("arialbd.ttf", 14)
    except Exception:
        font_logo = font_title = font_serif = font_sub = font_badge = ImageFont.load_default()

    # Brand text
    draw.text((card_margin_x + 88, card_margin_y + 57), "SDA STORE", fill=(250, 250, 250, 255), font=font_logo)

    # Title: PRE-PATCHED APPLICATIONS
    draw.text((card_margin_x + 50, card_margin_y + 115), "PRE-PATCHED", fill=(250, 250, 250, 255), font=font_title)
    draw.text((card_margin_x + 50, card_margin_y + 180), "APPLICATIONS", fill=(160, 160, 165, 255), font=font_serif)

    # Subtitle
    subtext = "High-Performance Patched Android APKs • Non-Root • Zero Modules"
    draw.text((card_margin_x + 50, card_margin_y + 265), subtext, fill=(161, 161, 170, 255), font=font_sub)

    subtext2 = "Curated Ad-Free Binaries, VIP Unlocks, Direct APK Downloads & Obtainium Auto-Updates"
    draw.text((card_margin_x + 50, card_margin_y + 300), subtext2, fill=(113, 113, 122, 255), font=font_sub)

    # Feature Chips
    chips = [
        ("✓ 100% Non-Root", (16, 185, 129)),
        ("⚡ 1-Tap Downloads", (56, 189, 248)),
        ("🛡️ Ad-Blocking & Privacy", (168, 85, 247)),
        ("🔄 Obtainium Tracking", (245, 158, 11)),
        ("📦 136 Verified Apps", (236, 72, 153))
    ]

    chip_x = card_margin_x + 50
    chip_y = card_margin_y + 380
    for label, col in chips:
        text_bbox = draw.textbbox((chip_x + 14, chip_y + 8), label, font=font_badge)
        chip_w = text_bbox[2] - chip_x + 14
        draw.rounded_rectangle(
            [(chip_x, chip_y), (chip_x + chip_w, chip_y + 36)],
            radius=18,
            fill=(24, 24, 27, 255),
            outline=(63, 63, 70, 255),
            width=1
        )
        draw.text((chip_x + 14, chip_y + 9), label, fill=(250, 250, 250, 255), font=font_badge)
        chip_x += chip_w + 14

    # Footer note inside card
    draw.line(
        [(card_margin_x + 50, card_margin_y + 440), (WIDTH - card_margin_x - 50, card_margin_y + 440)],
        fill=(39, 39, 42, 255),
        width=1
    )
    draw.text(
        (card_margin_x + 50, card_margin_y + 455),
        "sudarsansda.github.io/SDA-Store  •  Automated CI/CD via GitHub Actions",
        fill=(113, 113, 122, 255),
        font=font_badge
    )

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    img.save(OUTPUT_PATH, format='PNG', optimize=True)
    print(f"Generated social preview image: {OUTPUT_PATH} ({WIDTH}x{HEIGHT})")

if __name__ == '__main__':
    create_og_image()
