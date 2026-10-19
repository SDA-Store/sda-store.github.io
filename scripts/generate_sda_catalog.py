#!/usr/bin/env python3
"""
Convert sample/data.json and data/patches into full SDA Store data/apps.json.
Ensures ALL release and download URLs point ONLY to sudarsanSDA/SDA-Store.
"""

import json
import os
import re
from datetime import datetime, timezone

DATA_JSON_PATH = 'sample/data.json'
OUT_APPS_JSON = 'data/apps.json'
GITHUB_REPO = 'sudarsanSDA/SDA-Store'

# Category mapping based on app key / category
CATEGORY_MAP = {
    'moviebox': 'Media & Video',
    'youtube': 'Media & Video',
    'youtubemusic': 'Music & Audio',
    'reddit': 'Social & News',
    'twitter': 'Social & News',
    'instagram': 'Social & News',
    'tiktok': 'Social & News',
    'telegram': 'Social & News',
    'threads': 'Social & News',
    'facebook': 'Social & News',
    'messenger': 'Social & News',
    'bravebrowser': 'Tools & Privacy',
    'browser': 'Tools & Privacy',
    'edge': 'Tools & Privacy',
    'microsoftedge': 'Tools & Privacy',
    'duolingo': 'Education',
    'discord': 'Social & News',
    'photos': 'Tools & Privacy',
    'googlephotos': 'Tools & Privacy',
    'googlemaps': 'Tools & Privacy',
    'soundcloud': 'Music & Audio',
    'twitch': 'Media & Video',
    'netflix': 'Media & Video',
    'primevideo': 'Media & Video',
    'disneyplus': 'Media & Video',
    'hbomax': 'Media & Video',
    'peacock': 'Media & Video',
    'plutotv': 'Media & Video',
    'tubi': 'Media & Video',
    'vix': 'Media & Video',
    'pandora': 'Music & Audio',
    'poweramp': 'Music & Audio',
    'podcastaddict': 'Music & Audio',
    'pocketcasts': 'Music & Audio',
    'symfonium': 'Music & Audio',
    'protonvpn': 'Tools & Privacy',
    'protonmail': 'Tools & Privacy',
    'adguard': 'Tools & Privacy',
    'macrodroid': 'Tools & Privacy',
    'cloudflarewarp': 'Tools & Privacy',
    'vpnify': 'Tools & Privacy',
    'solidexplorer': 'Tools & Privacy',
    'sdmaid2se': 'Tools & Privacy',
    'photomath': 'Education',
}

# Icon mapping for popular apps (high quality SVGs from dashboard-icons / simple-icons)
ICON_MAP = {
    'moviebox': 'https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/svg/plex.svg',
    'youtube': 'https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/svg/youtube.svg',
    'youtubemusic': 'https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/svg/youtube-music.svg',
    'reddit': 'https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/svg/reddit.svg',
    'twitter': 'https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/svg/twitter.svg',
    'instagram': 'https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/svg/instagram.svg',
    'tiktok': 'https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/svg/tiktok.svg',
    'telegram': 'https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/svg/telegram.svg',
    'facebook': 'https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/svg/facebook.svg',
    'messenger': 'https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/svg/facebook-messenger.svg',
    'bravebrowser': 'https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/svg/brave.svg',
    'microsoftedge': 'https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/svg/microsoft-edge.svg',
    'duolingo': 'https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/svg/duolingo.svg',
    'discord': 'https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/svg/discord.svg',
    'googlephotos': 'https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/svg/google-photos.svg',
    'photos': 'https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/svg/google-photos.svg',
    'googlemaps': 'https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/svg/google-maps.svg',
    'soundcloud': 'https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/svg/soundcloud.svg',
    'twitch': 'https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/svg/twitch.svg',
    'netflix': 'https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/svg/netflix.svg',
    'primevideo': 'https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/svg/prime-video.svg',
    'disneyplus': 'https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/svg/disneyplus.svg',
    'protonvpn': 'https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/svg/protonvpn.svg',
    'protonmail': 'https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/svg/protonmail.svg',
    'adguard': 'https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/svg/adguard-home.svg',
    'github': 'https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/svg/github.svg',
    'spotify': 'https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/svg/spotify.svg',
}

def guess_category(app_key, app_name):
    key = app_key.lower().replace('-', '').replace('_', '')
    if key in CATEGORY_MAP:
        return CATEGORY_MAP[key]
    for k, cat in CATEGORY_MAP.items():
        if k in key or k in app_name.lower():
            return cat
    
    # Generic heuristics
    name_l = app_name.lower()
    if any(w in name_l for w in ['player', 'tv', 'video', 'stream', 'movie', 'cinema', 'watch']):
        return 'Media & Video'
    if any(w in name_l for w in ['music', 'audio', 'sound', 'podcast', 'radio', 'beats']):
        return 'Music & Audio'
    if any(w in name_l for w in ['social', 'chat', 'message', 'feed', 'post', 'forum', 'news', 'reader']):
        return 'Social & News'
    if any(w in name_l for w in ['learn', 'study', 'dict', 'math', 'lang', 'chinese', 'fit', 'gym', 'workout']):
        return 'Education'
    return 'Tools & Privacy'

def generate_catalog():
    with open(DATA_JSON_PATH, 'r', encoding='utf-8') as f:
        src = json.load(f)

    patch_sets = src.get('patchSets', [])
    src_apps = src.get('apps', [])

    sda_apps = []

    # 1. MovieBox (Flagship at the very top)
    moviebox_entry = {
        "id": "moviebox",
        "name": "MovieBox",
        "category": "Media & Video",
        "brand": "SDA Store",
        "version": "6",
        "releaseUrl": f"https://github.com/{GITHUB_REPO}/releases/tag/v6",
        "publishedAt": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        "icon": "assets/icons/moviebox.svg",
        "description": "Patched MovieBox by SDA Store with ad-removal, VIP streaming unlock, download enable, and UI decluttering.",
        "patchCount": 4,
        "patches": [
            "All-In-One (Playback & download enable, ad removal, VIP unlock)",
            "Hide BuzzBox tabs from bottom navigation",
            "Hide Midnight 18+ tab from home",
            "Hide permanent foreground notification"
        ],
        "assets": [
            {
                "name": "moviebox-patched-arm64-v8a.apk",
                "arch": "arm64",
                "version": "5",
                "size": 68151874,
                "downloadUrl": f"https://github.com/{GITHUB_REPO}/releases/download/v5/moviebox-patched-arm64-v8a.apk"
            }
        ]
    }
    sda_apps.append(moviebox_entry)

    # 2. Process all apps from sample/data.json
    for a in src_apps:
        app_key = a.get('appKey', '').lower()
        if app_key == 'moviebox':
            continue  # Already inserted our custom tuned MovieBox

        app_name = a.get('appName', '')
        brands = a.get('brands', [])
        if not brands:
            continue

        # Preferred brand selection:
        # Prefer 'Morphe' or 'anddea' or 'rushiranpise' or first brand
        pref_brand = None
        for b in brands:
            bname = b.get('brandName', '').lower()
            if 'morphe' in bname or 'anddea' in bname or 'rushiranpise' in bname or 'hush' in bname:
                pref_brand = b
                break
        if not pref_brand:
            pref_brand = brands[0]

        brand_name = pref_brand.get('brandName', '')
        version = pref_brand.get('latestVersion', 'latest')

        # Extract builds and patches
        builds = pref_brand.get('builds', [])
        patches = []
        if builds:
            latest_b = builds[0]
            pref_idx = latest_b.get('patchSetRef')
            if pref_idx is not None and pref_idx < len(patch_sets):
                patches = patch_sets[pref_idx]
            if not patches:
                for bld in builds:
                    idx = bld.get('patchSetRef')
                    if idx is not None and idx < len(patch_sets) and patch_sets[idx]:
                        patches = patch_sets[idx]
                        break

        # Assets
        assets = []
        if builds:
            for bld in builds[:2]:
                for ast in bld.get('assets', []):
                    fname = ast.get('name', '')
                    if not fname.endswith('.apk'):
                        continue  # Exclude .zip Magisk modules from APK cards
                    arch_raw = ast.get('arch', 'arm64')
                    arch = 'arm64' if '64' in arch_raw else ('arm' if 'arm' in arch_raw or 'v7' in arch_raw else 'universal')
                    ast_ver = ast.get('version', version)
                    size = ast.get('size', 0)

                    arch_suffix = 'arm64-v8a' if arch == 'arm64' else ('arm-v7a' if arch == 'arm' else 'universal')
                    clean_fname = f"{app_key}-sda-v{ast_ver}-{arch_suffix}.apk"

                    # SDA Store release download URL
                    sda_download_url = f"https://github.com/{GITHUB_REPO}/releases/download/v{ast_ver}/{clean_fname}"

                    # Avoid duplicate archs
                    if not any(x['arch'] == arch for x in assets):
                        assets.append({
                            "name": clean_fname,
                            "arch": arch,
                            "version": str(ast_ver),
                            "size": size,
                            "downloadUrl": sda_download_url
                        })

        if not assets:
            # Generate default asset row
            std_name = f"{app_key}-sda-v{version}-arm64-v8a.apk"
            assets.append({
                "name": std_name,
                "arch": "arm64",
                "version": str(version),
                "size": 52428800,
                "downloadUrl": f"https://github.com/{GITHUB_REPO}/releases/download/v{version}/{std_name}"
            })

        category = guess_category(app_key, app_name)
        icon_url = ICON_MAP.get(app_key) or f"https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/svg/{app_key}.svg"

        # Generate clean description with full credit to SDA Store
        desc = f"Patched {app_name} by SDA Store with premium feature unlock, ad-free experience, privacy enhancements, and zero tracking."

        sda_apps.append({
            "id": app_key,
            "name": app_name,
            "category": category,
            "brand": "SDA Store",
            "version": str(version),
            "releaseUrl": f"https://github.com/{GITHUB_REPO}/releases",
            "publishedAt": a.get('latestPublishedAt') or datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
            "icon": icon_url,
            "description": desc,
            "patchCount": len(patches),
            "patches": patches if patches else [
                "Ad-blocking & sponsored content removal",
                "Background playback & minimize support",
                "Telemetry, analytics & tracker blocking",
                "Premium feature unlocking",
                "Pure clean interface & decluttering"
            ],
            "assets": assets
        })

    output_data = {
        "storeName": "SDA Store",
        "storeDescription": "Fast, modern catalog for clean, automated patched Android APKs.",
        "updatedAt": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        "appsCount": len(sda_apps),
        "apps": sda_apps
    }

    with open(OUT_APPS_JSON, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"Successfully generated {OUT_APPS_JSON} with {len(sda_apps)} applications!")

if __name__ == '__main__':
    generate_catalog()
