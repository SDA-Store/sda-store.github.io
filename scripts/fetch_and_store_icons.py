#!/usr/bin/env python3
"""
Fetch and store official high-res icons for all apps in data/apps.json.
Saves local files into assets/icons/<app_id>.png or .svg.
Updates data/apps.json to reference local assets.
"""

import os
import json
import re
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

ICONS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'icons')
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'apps.json')
PATCHES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'patches')

os.makedirs(ICONS_DIR, exist_ok=True)

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"

# Curated High-Res SVGs for top tier brands
CURATED_SVGS = {
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
    'spotify': 'https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/svg/spotify.svg',
    'github': 'https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/svg/github.svg',
}

# Domain mapping for Google S2 Favicon High-Res resolution
DOMAIN_MAP = {
    'capcut': 'capcut.com',
    'accuweather': 'accuweather.com',
    'camscanner': 'camscanner.com',
    'inshot': 'inshot.com',
    'picsart': 'picsart.com',
    'calm': 'calm.com',
    'chesscom': 'chess.com',
    'aliexpress': 'aliexpress.com',
    'amazonindia': 'amazon.in',
    'amazonshopping': 'amazon.com',
    'appsales': 'app-sales.net',
    'at4klauncher': 'androidtv.com',
    'automate': 'llamalab.com',
    'autosync': 'metactrl.com',
    'backdrops': 'backdrops.io',
    'batteryguru': 'paget96projects.com',
    'betamaniac': 'google.com',
    'citymapper': 'citymapper.com',
    'cloudflarewarp': 'cloudflare.com',
    'cricbuzz': 'cricbuzz.com',
    'eyecon': 'eyecon-app.com',
    'fairemail': 'email.faircode.eu',
    'fing': 'fing.com',
    'flipkart': 'flipkart.com',
    'foldersync': 'tacit.dk',
    'gboard': 'google.com',
    'goodreads': 'goodreads.com',
    'googlenews': 'news.google.com',
    'googlephone': 'google.com',
    'googlerecorder': 'google.com',
    'hbomax': 'max.com',
    'hellochinese': 'hellochinese.com',
    'hermit': 'chimbori.com',
    'holavpn': 'hola.org',
    'ibispaintx': 'ibispaint.com',
    'imdb': 'imdb.com',
    'inshorts': 'inshorts.com',
    'kinestop': 'kinestop.com',
    'komoot': 'komoot.com',
    'letterboxd': 'letterboxd.com',
    'linkedin': 'linkedin.com',
    'luminawallpapers': 'google.com',
    'macrodroid': 'macrodroid.com',
    'medium': 'medium.com',
    'meesho': 'meesho.com',
    'merriamwebsterdictionary': 'merriam-webster.com',
    'microsoftlens': 'microsoft.com',
    'microsoftswiftkey': 'microsoft.com',
    'moneymanager': 'realbyteapps.com',
    'moonreader': 'moondownload.com',
    'myexpenses': 'myexpenses.mobi',
    'myfitnesspal': 'myfitnesspal.com',
    'niagaralauncher': 'niagaralauncher.app',
    'ninjavpn': 'ninjavpn.com',
    'novalauncher': 'novalauncher.com',
    'nuvio': 'nuvio.app',
    'offlinegames': 'google.com',
    'pandora': 'pandora.com',
    'peacock': 'peacocktv.com',
    'photomath': 'photomath.com',
    'pinterest': 'pinterest.com',
    'pixiv': 'pixiv.net',
    'plusmessenger': 'plusmessenger.org',
    'plutotv': 'pluto.tv',
    'pocketcasts': 'pocketcasts.com',
    'podcastaddict': 'podcastaddict.com',
    'poweramp': 'powerampapp.com',
    'protonpass': 'proton.me',
    'rar': 'rarlab.com',
    'rumble': 'rumble.com',
    'sdmaid2se': 'github.com',
    'sendfilestotv': 'sendfilestotv.app',
    'showly': 'showly.app',
    'smartlauncher6': 'smartlauncher.net',
    'sofascore': 'sofascore.com',
    'solidexplorer': 'neatbytes.com',
    'speedtest': 'speedtest.net',
    'strava': 'strava.com',
    'swiftbackup': 'swiftbackup.net',
    'symfonium': 'symfonium.app',
    'terabox': 'terabox.com',
    'termius': 'termius.com',
    'theweatherchannel': 'weather.com',
    'threads': 'threads.net',
    'ticktick': 'ticktick.com',
    'titaniumbrowser': 'google.com',
    'todoist': 'todoist.com',
    'trakttv': 'trakt.tv',
    'truecaller': 'truecaller.com',
    'tubi': 'tubitv.com',
    'tumblr': 'tumblr.com',
    'ventusky': 'ventusky.com',
    'viber': 'viber.com',
    'vix': 'vix.com',
    'vpnify': 'vpnify.app',
    'wallcraft': 'wallcraft.com',
    'windscribevpn': 'windscribe.com',
    'wpsoffice': 'wps.com',
    'xodo': 'xodo.com',
    'xrecorder': 'inshot.com',
}

def extract_package_from_toml(app_id):
    if not os.path.exists(PATCHES_DIR):
        return None
    for f in os.listdir(PATCHES_DIR):
        if f.endswith('.toml'):
            path = os.path.join(PATCHES_DIR, f)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
                    content = fp.read()
                    if app_id in f.lower() or app_id in content.lower():
                        m = re.search(r'pkg-name\s*=\s*"([^"]+)"', content)
                        if m:
                            return m.group(1)
            except Exception:
                pass
    return None

def fetch_google_play_icon(pkg):
    if not pkg:
        return None
    url = f"https://play.google.com/store/apps/details?id={pkg}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
        with urllib.request.urlopen(req, timeout=8) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            m = re.search(r'property="og:image"\s+content="([^"]+)"', html)
            if not m:
                m = re.search(r'content="([^"]+)"\s+property="og:image"', html)
            if m:
                icon_url = m.group(1)
                if '=s' in icon_url:
                    icon_url = re.sub(r'=s\d+.*$', '=s256', icon_url)
                return icon_url
    except Exception:
        pass
    return None

def fetch_google_favicon(domain):
    return f"https://www.google.com/s2/favicons?domain={domain}&sz=128"

def generate_svg_monogram(app_name):
    # Elegant monochromatic rounded squircle badge with initial letters
    initials = "".join([w[0].upper() for w in app_name.split()[:2]]) if app_name else "A"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#27272a" />
      <stop offset="100%" stop-color="#09090b" />
    </linearGradient>
  </defs>
  <rect width="100" height="100" rx="26" fill="url(#grad)" stroke="#3f3f46" stroke-width="2"/>
  <text x="50" y="60" text-anchor="middle" fill="#fafafa" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-weight="800" font-size="34" letter-spacing="-1">{initials}</text>
</svg>'''

def download_and_save(url, dest_path):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
        with urllib.request.urlopen(req, timeout=12) as resp:
            content = resp.read()
            if len(content) > 200:
                with open(dest_path, 'wb') as f:
                    f.write(content)
                return True
    except Exception:
        pass
    return False

def process_app(app):
    app_id = app.get('id', '').lower()
    app_name = app.get('name', '')
    dest_file = f"{app_id}.png"
    dest_path = os.path.join(ICONS_DIR, dest_file)
    svg_dest = os.path.join(ICONS_DIR, f"{app_id}.svg")

    # If already cached and valid size (>500 bytes)
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 500:
        app['icon'] = f"assets/icons/{dest_file}"
        return
    if os.path.exists(svg_dest) and os.path.getsize(svg_dest) > 200:
        app['icon'] = f"assets/icons/{app_id}.svg"
        return

    # 1. Try Curated High-Res SVG
    if app_id in CURATED_SVGS:
        if download_and_save(CURATED_SVGS[app_id], svg_dest):
            app['icon'] = f"assets/icons/{app_id}.svg"
            print(f"[CURATED] Saved {app_name} -> {app_id}.svg")
            return

    # 2. Try Google Play Store by Package Name
    pkg = extract_package_from_toml(app_id)
    play_icon = fetch_google_play_icon(pkg)
    if play_icon:
        if download_and_save(play_icon, dest_path):
            app['icon'] = f"assets/icons/{dest_file}"
            print(f"[PLAY] Saved {app_name} -> {dest_file}")
            return

    # 3. Try Google S2 Favicon by Domain
    domain = DOMAIN_MAP.get(app_id)
    if not domain:
        clean_name = re.sub(r'[^a-zA-Z0-9]', '', app_name.lower())
        domain = f"{clean_name}.com"

    fav_url = fetch_google_favicon(domain)
    if download_and_save(fav_url, dest_path):
        app['icon'] = f"assets/icons/{dest_file}"
        print(f"[FAVICON] Saved {app_name} -> {dest_file}")
        return

    # 4. Fallback to Beautiful Styled SVG Monogram
    with open(svg_dest, 'w', encoding='utf-8') as f:
        f.write(generate_svg_monogram(app_name))
    app['icon'] = f"assets/icons/{app_id}.svg"
    print(f"[MONOGRAM] Created {app_name} -> {app_id}.svg")

def main():
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        catalog = json.load(f)

    apps = catalog.get('apps', [])
    print(f"Processing icons for {len(apps)} apps in parallel...")

    with ThreadPoolExecutor(max_workers=16) as pool:
        pool.map(process_app, apps)

    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    print("Icon processing completed and data/apps.json updated successfully!")

if __name__ == '__main__':
    main()
