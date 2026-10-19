#!/usr/bin/env python3
"""
SDA Store - Comprehensive SEO & AI Sitemaps Generator
Generates:
1. sitemap.xml (Standard XML Sitemap for Google, Bing, DuckDuckGo)
2. llms.txt (Official AI/LLM discovery manifest for Perplexity, ChatGPT, Claude, Gemini)
3. llms-full.txt (Complete detailed index for AI search engines)
4. robots.txt (Search engine & AI crawler directives)
5. feed.xml (RSS 2.0 Syndication Feed for rapid indexing)
6. .well-known/ai-plugin.json (Standard AI Agent / Assistant Plugin Manifest)
"""

import os
import json
import re
from datetime import datetime, timezone
import xml.etree.ElementTree as ET

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS_JSON = os.path.join(BASE_DIR, 'data', 'apps.json')
BASE_URL = "https://sudarsansda.github.io/SDA-Store"
ROOT_URL = "https://sudarsansda.github.io"

def load_catalog():
    if not os.path.exists(APPS_JSON):
        raise FileNotFoundError(f"Missing {APPS_JSON}")
    with open(APPS_JSON, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_sitemap_xml(catalog):
    """Generate standard XML Sitemap with all 136 apps and sections."""
    now_iso = datetime.now(timezone.utc).strftime('%Y-%m-%d')

    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
        '        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">'
    ]

    # Main Pages
    pages = [
        (f"{BASE_URL}/", "1.0", "daily"),
        (f"{BASE_URL}/#catalog", "0.9", "daily"),
        (f"{BASE_URL}/#utilities", "0.8", "weekly"),
        (f"{ROOT_URL}/", "0.9", "daily"),
    ]

    for loc, priority, changefreq in pages:
        xml_lines.append('  <url>')
        xml_lines.append(f'    <loc>{loc}</loc>')
        xml_lines.append(f'    <lastmod>{now_iso}</lastmod>')
        xml_lines.append(f'    <changefreq>{changefreq}</changefreq>')
        xml_lines.append(f'    <priority>{priority}</priority>')
        xml_lines.append('  </url>')

    # Deep links for each application in the catalog
    for app in catalog.get('apps', []):
        app_id = app.get('id', '')
        if not app_id:
            continue
        pub_at = app.get('publishedAt', '')
        lastmod = pub_at[:10] if pub_at else now_iso
        app_url = f"{BASE_URL}/?app={app_id}"

        # Flagships get higher priority
        priority = "0.9" if app_id in ['moviebox', 'youtube', 'youtubemusic', 'reddit', 'cricbuzz', 'discord', 'twitter', 'instagram'] else "0.7"

        xml_lines.append('  <url>')
        xml_lines.append(f'    <loc>{app_url}</loc>')
        xml_lines.append(f'    <lastmod>{lastmod}</lastmod>')
        xml_lines.append('    <changefreq>weekly</changefreq>')
        xml_lines.append(f'    <priority>{priority}</priority>')
        xml_lines.append('  </url>')

    xml_lines.append('</urlset>')
    sitemap_content = '\n'.join(xml_lines)

    output_path = os.path.join(BASE_DIR, 'sitemap.xml')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(sitemap_content)
    print(f"Generated {output_path} with {len(catalog.get('apps', [])) + len(pages)} URLs.")

def generate_llms_txt(catalog):
    """
    Generate /llms.txt following the official Jeremy Howard / LLMS.txt standard.
    Used by Perplexity, ChatGPT Search, Claude, Gemini to parse website context.
    """
    apps = catalog.get('apps', [])
    categories = sorted(list(set(a.get('category', 'Tools & Privacy') for a in apps)))
    flagships = ['moviebox', 'cricbuzz', 'youtube', 'youtubemusic', 'reddit', 'discord', 'twitter', 'instagram', 'bravebrowser', 'spotify']
    flagship_apps = [a for a in apps if a.get('id') in flagships]

    lines = [
        "# SDA Store",
        "",
        "> High-Performance, Minimalist Catalog for Curated Patched Android Binaries.",
        "> Non-root binaries, zero telemetry, direct APK downloads, and Obtainium auto-updates.",
        "",
        "## Overview",
        "",
        "SDA Store is an open, curated catalog of 136+ verified patched Android applications.",
        "Every APK is clean, non-root, and built with ad-removal, telemetry stripping, background playback, and premium features unlocked.",
        "Builds are automatically compiled and published through GitHub Actions CI pipelines.",
        "",
        "## Key Features",
        "",
        "- **100% Non-Root**: Works on any Android phone without root access or custom ROMs.",
        "- **Zero Modules**: Self-contained APKs that install directly without Magisk or Xposed.",
        "- **Direct APK Downloads**: Clean, direct downloads for instant 1-tap installation.",
        "- **Obtainium Integration**: Built-in 1-tap tracking via Obtainium for instant background update notifications directly from GitHub Releases.",
        "- **Full Privacy**: Tracking libraries, Google Analytics, and ad-networks removed.",
        "",
        "## Flagship Applications",
        ""
    ]

    for app in flagship_apps:
        v = app.get('version', 'Latest')
        lines.append(f"- [{app['name']}]({BASE_URL}/?app={app['id']}): v{v} • {app['description']}")

    lines.extend([
        "",
        "## Available Categories",
        ""
    ])
    for cat in categories:
        count = sum(1 for a in apps if a.get('category') == cat)
        lines.append(f"- **{cat}**: {count} applications available.")

    lines.extend([
        "",
        "## Direct Links & Resources",
        "",
        f"- [Full Application Index ({len(apps)} Apps)]({BASE_URL}/llms-full.txt)",
        f"- [Web Catalog Interface]({BASE_URL}/)",
        f"- [XML Sitemap]({BASE_URL}/sitemap.xml)",
        f"- [RSS Release Feed]({BASE_URL}/feed.xml)",
        "- [GitHub Repository & CI Pipelines](https://github.com/sudarsanSDA/SDA-Store)",
        "- [GitHub Releases (Direct Binaries)](https://github.com/sudarsanSDA/SDA-Store/releases)",
        "- [Obtainium Open-Source Updater](https://github.com/ImranR98/Obtainium)"
    ])

    content = '\n'.join(lines)
    output_path = os.path.join(BASE_DIR, 'llms.txt')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Generated {output_path}.")

def generate_llms_full_txt(catalog):
    """Generate detailed /llms-full.txt containing complete technical metadata for all 136 apps."""
    apps = catalog.get('apps', [])
    now_iso = datetime.now(timezone.utc).strftime('%Y-%m-%d')

    lines = [
        "# SDA Store - Complete Application Catalog",
        f"# Last Updated: {now_iso}",
        f"# Total Applications: {len(apps)}",
        "",
        "This document provides the complete machine-readable index of all patched applications in SDA Store.",
        ""
    ]

    for i, app in enumerate(apps, 1):
        name = app.get('name', 'Unknown')
        app_id = app.get('id', '')
        version = app.get('version', 'Latest')
        category = app.get('category', 'Tools & Privacy')
        desc = app.get('description', '')
        patches = app.get('patches', [])
        assets = app.get('assets', [])

        lines.append(f"## {i}. {name} (v{version})")
        lines.append(f"- **App ID**: `{app_id}`")
        lines.append(f"- **Category**: {category}")
        lines.append(f"- **Description**: {desc}")
        lines.append(f"- **Catalog Link**: {BASE_URL}/?app={app_id}")
        
        if patches:
            lines.append("- **Applied Patches**:")
            for p in patches[:6]:
                lines.append(f"  - {p}")
            if len(patches) > 6:
                lines.append(f"  - *...and {len(patches) - 6} more patches*")

        if assets:
            lines.append("- **Direct Download Assets**:")
            for ast in assets:
                aname = ast.get('name', 'app.apk')
                arch = ast.get('arch', 'arm64')
                dl = ast.get('downloadUrl', '#')
                lines.append(f"  - [{aname} ({arch.upper()})]({dl})")
        lines.append("")

    content = '\n'.join(lines)
    output_path = os.path.join(BASE_DIR, 'llms-full.txt')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Generated {output_path} with {len(apps)} apps.")

def generate_robots_txt():
    """Generate modern robots.txt welcoming all standard & AI search crawlers."""
    content = f"""# Robots.txt for SDA Store
# Optimized for Google, Bing, DuckDuckGo, and Modern AI Search Engines (Perplexity, ChatGPT, Claude)

User-agent: *
Allow: /
Allow: /index.html
Allow: /data/
Allow: /assets/
Allow: /css/
Allow: /js/
Allow: /sitemap.xml
Allow: /llms.txt
Allow: /llms-full.txt
Allow: /feed.xml

# Explicitly Authorize AI & LLM Search Agents
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: CCBot
Allow: /

User-agent: cohere-ai
Allow: /

User-agent: Diffbot
Allow: /

# Sitemaps and AI Manifest References
Sitemap: {BASE_URL}/sitemap.xml
Sitemap: {ROOT_URL}/sitemap.xml
AI-Content: {BASE_URL}/llms.txt
AI-Full-Content: {BASE_URL}/llms-full.txt
"""
    output_path = os.path.join(BASE_DIR, 'robots.txt')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')
    print(f"Generated {output_path}.")

def generate_feed_xml(catalog):
    """Generate RSS 2.0 / Atom syndication feed for search engines."""
    apps = catalog.get('apps', [])
    now_rfc = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')

    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">',
        '  <channel>',
        '    <title>SDA Store — Latest Patched Android APK Releases</title>',
        f'    <link>{BASE_URL}/</link>',
        '    <description>Curated catalog of verified, safe, non-root patched Android APKs with ad-removal, VIP streaming, and zero telemetry.</description>',
        '    <language>en-us</language>',
        f'    <lastBuildDate>{now_rfc}</lastBuildDate>',
        f'    <atom:link href="{BASE_URL}/feed.xml" rel="self" type="application/rss+xml"/>',
    ]

    for app in apps[:30]:  # Top 30 recent releases in feed
        name = app.get('name', 'App')
        version = app.get('version', 'Latest')
        desc = app.get('description', '')
        link = f"{BASE_URL}/?app={app.get('id', '')}"
        guid = f"sda-store-{app.get('id', '')}-{version}"
        pub_date = now_rfc

        xml_lines.extend([
            '    <item>',
            f'      <title><![CDATA[{name} v{version} (Patched APK)]]></title>',
            f'      <link>{link}</link>',
            f'      <guid isPermaLink="false">{guid}</guid>',
            f'      <description><![CDATA[{desc}]]></description>',
            f'      <pubDate>{pub_date}</pubDate>',
            '    </item>'
        ])

    xml_lines.extend([
        '  </channel>',
        '</rss>'
    ])

    output_path = os.path.join(BASE_DIR, 'feed.xml')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(xml_lines))
    print(f"Generated {output_path}.")

def generate_ai_plugin_json():
    """Generate standard .well-known/ai-plugin.json manifest."""
    plugin_dir = os.path.join(BASE_DIR, '.well-known')
    os.makedirs(plugin_dir, exist_ok=True)

    manifest = {
        "schema_version": "v1",
        "name_for_human": "SDA Store",
        "name_for_model": "sda_store",
        "description_for_human": "Browse and download curated, ad-free, non-root patched Android APKs.",
        "description_for_model": "Plugin and manifest for searching, exploring, and retrieving patched Android APK metadata, download links, and patch lists from SDA Store.",
        "auth": {
            "type": "none"
        },
        "api": {
            "type": "openapi",
            "url": f"{BASE_URL}/data/apps.json"
        },
        "logo_url": f"{BASE_URL}/assets/icons/moviebox.svg",
        "contact_email": "sudarsan@sda.store",
        "legal_info_url": f"{BASE_URL}/#utilities"
    }

    output_path = os.path.join(plugin_dir, 'ai-plugin.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)
    print(f"Generated {output_path}.")

def inject_noscript_catalog(catalog):
    """
    Injects or updates a pre-rendered semantic <noscript> catalog inside index.html.
    This guarantees 100% crawlability and SEO indexing for search bots and AI crawlers
    (Perplexity, ChatGPT, Googlebot, Bingbot) that do not evaluate client-side JavaScript.
    """
    index_html_path = os.path.join(BASE_DIR, 'index.html')
    if not os.path.exists(index_html_path):
        return

    with open(index_html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    apps = catalog.get('apps', [])
    categories = sorted(list(set(a.get('category', 'Tools & Privacy') for a in apps)))

    noscript_lines = [
        '        <!-- NOSCRIPT_CATALOG_START -->',
        '        <!-- Pre-rendered Semantic SEO Catalog for Search Engines & AI Crawlers -->',
        '        <noscript>',
        '            <section class="noscript-catalog" style="padding: 2.5rem 1.5rem; max-width: 1200px; margin: 2rem auto; border-top: 1px solid rgba(0,0,0,0.1);">',
        '                <h2 style="font-size: 1.5rem; margin-bottom: 0.5rem;">SDA Store — Patched Android Applications Directory</h2>',
        f'                <p style="margin-bottom: 1.5rem;">Browse all {len(apps)} curated, non-root patched Android APKs with ad-blocking, privacy protections, and zero telemetry.</p>'
    ]

    for cat in categories:
        cat_apps = [a for a in apps if a.get('category') == cat]
        noscript_lines.append(f'                <div style="margin-bottom: 2rem;">')
        noscript_lines.append(f'                    <h3 style="font-size: 1.15rem; margin-bottom: 0.75rem; border-bottom: 1px solid rgba(0,0,0,0.08); padding-bottom: 0.35rem;">{cat} ({len(cat_apps)} Apps)</h3>')
        noscript_lines.append(f'                    <ul style="list-style: none; padding: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 0.85rem;">')
        for app in cat_apps:
            app_id = app.get('id', '')
            name = app.get('name', 'App')
            version = app.get('version', 'Latest')
            desc = app.get('description', '')
            link = f"{BASE_URL}/?app={app_id}"
            assets = app.get('assets', [])
            dl_link = assets[0].get('downloadUrl', link) if assets else link
            arch = assets[0].get('arch', 'arm64').upper() if assets else 'ARM64'
            
            noscript_lines.append(f'                        <li style="padding: 0.85rem; border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;">')
            noscript_lines.append(f'                            <strong><a href="{link}">{name}</a></strong> <small>v{version}</small>')
            noscript_lines.append(f'                            <p style="font-size: 0.85rem; margin: 0.4rem 0;">{desc}</p>')
            noscript_lines.append(f'                            <a href="{dl_link}" style="font-size: 0.8rem; font-weight: 600;">Direct APK Download ({arch})</a>')
            noscript_lines.append(f'                        </li>')
        noscript_lines.append('                    </ul>')
        noscript_lines.append('                </div>')

    noscript_lines.append('            </section>')
    noscript_lines.append('        </noscript>')
    noscript_lines.append('        <!-- NOSCRIPT_CATALOG_END -->')

    noscript_block = '\n'.join(noscript_lines)

    if '<!-- NOSCRIPT_CATALOG_START -->' in html_content and '<!-- NOSCRIPT_CATALOG_END -->' in html_content:
        pattern = re.compile(r'(\s*)<!-- NOSCRIPT_CATALOG_START -->.*?<!-- NOSCRIPT_CATALOG_END -->', re.DOTALL)
        new_html = pattern.sub(f'\n{noscript_block}', html_content)
    else:
        new_html = html_content.replace('</main>', f'{noscript_block}\n    </main>')

    with open(index_html_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f"Injected semantic <noscript> catalog ({len(apps)} apps) into {index_html_path}.")

def main():
    print("==================================================")
    print("  SDA Store - SEO & AI Sitemaps Generator")
    print("==================================================")
    catalog = load_catalog()
    generate_sitemap_xml(catalog)
    generate_llms_txt(catalog)
    generate_llms_full_txt(catalog)
    generate_robots_txt()
    generate_feed_xml(catalog)
    generate_ai_plugin_json()
    inject_noscript_catalog(catalog)
    print("All SEO & AI sitemaps generated successfully!")

if __name__ == '__main__':
    main()
