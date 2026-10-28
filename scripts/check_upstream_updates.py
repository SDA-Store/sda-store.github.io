#!/usr/bin/env python3
"""
SDA Store - Upstream Update Watcher & Auto-Dispatch
Monitors upstream patch sources (Morphe, ReVanced) and base APK releases (MovieBox, YouTube, Reddit, etc.).
When a new APK or patch version is detected:
1. Updates data/upstream_state.json
2. Automatically triggers GitHub Actions build-and-release workflow for each updated app.
"""

import os
import sys
import json
import re
import subprocess
import urllib.request
import urllib.parse

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
STATE_FILE = os.path.join(BASE_DIR, 'data', 'upstream_state.json')
APPS_JSON = os.path.join(BASE_DIR, 'data', 'apps.json')
PATCHES_DIR = os.path.join(BASE_DIR, 'data', 'patches')

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"

def get_headers():
    headers = {'User-Agent': USER_AGENT}
    token = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    if token:
        headers['Authorization'] = f"token {token}"
    return headers

def fetch_json(url):
    try:
        req = urllib.request.Request(url, headers=get_headers())
        with urllib.request.urlopen(req, timeout=12) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f"Error fetching JSON from {url}: {e}")
        return None

def fetch_text(url):
    try:
        req = urllib.request.Request(url, headers=get_headers())
        with urllib.request.urlopen(req, timeout=12) as resp:
            return resp.read().decode('utf-8', errors='ignore')
    except Exception as e:
        return ""

def get_latest_github_release(repo):
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    data = fetch_json(url)
    if data and 'tag_name' in data:
        return data['tag_name']
    return None

def get_moviebox_latest_version():
    try:
        # Check official CDN redirect URL for MovieBox
        url = "https://h5-api.aoneroom.com/pkg/redirect"
        req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
        # Don't auto follow redirect so we can inspect Location header
        class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, req, fp, code, msg, headers, newurl):
                return None
        opener = urllib.request.build_opener(NoRedirectHandler)
        try:
            resp = opener.open(req, timeout=10)
        except urllib.error.HTTPError as e:
            if e.code in (301, 302, 303, 307, 308):
                loc = e.headers.get('Location', '')
                m = re.search(r'v-?(\d+(?:\.\d+)+)', loc)
                if m:
                    return m.group(1)
        # Fallback to current verified MovieBox version
        return "4.0.03.1022.03"
    except Exception:
        return "4.0.03.1022.03"

def get_uptodown_version(uptodown_url):
    if not uptodown_url:
        return None
    html = fetch_text(uptodown_url)
    if not html:
        return None
    m = re.search(r'class="version"[^>]*>([^<]+)<', html) or re.search(r'itemprop="version"[^>]*>([^<]+)<', html)
    if m:
        v = m.group(1).strip()
        v = re.sub(r'\s*-\s*(Stable|Release|Beta).*$', '', v, flags=re.I).strip()
        return v
    # Fallback regex search for version pattern in top block
    m2 = re.findall(r'\b\d+\.\d+(?:\.\d+)+\b', html[:15000])
    if m2:
        return m2[0]
    return None

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "morphe_patches": "",
        "revanced_patches": "",
        "apps": {}
    }

def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2)

def parse_version(v):
    if not v:
        return ()
    nums = re.findall(r'\d+', str(v))
    return tuple(int(x) for x in nums)

def is_newer_version(new_v, current_v):
    if not current_v:
        return bool(new_v)
    if not new_v:
        return False
    return parse_version(new_v) > parse_version(current_v)

# Applications supported for automated headless building in GitHub Actions CI
AUTONOMOUS_BUILD_APPS = {'moviebox', 'youtube', 'youtubemusic', 'reddit'}

def main():
    trigger_actions = "--trigger" in sys.argv
    state = load_state()
    updated_apps = set()

    print("==================================================")
    print("  SDA Store - Upstream Update Watcher")
    print("==================================================")

    # 1. Check Patch Engines & Bundles
    print("Checking upstream patch releases...")
    latest_morphe_app = get_latest_github_release("MorpheApp/morphe-patches") or "v1.48.0"
    latest_morphe_hx = get_latest_github_release("hxreborn/morphe-patches") or "v1.59.0"
    latest_revanced = get_latest_github_release("inotia00/revanced-patches") or "v5.14.1"

    curr_morphe_app = state.get('morphe_app_patches', '')
    curr_morphe_hx = state.get('morphe_hx_patches', '')
    curr_revanced = state.get('revanced_patches', '')

    print(f"Morphe YouTube Patches (MorpheApp): current={curr_morphe_app} | upstream={latest_morphe_app}")
    print(f"Morphe MovieBox Patches (hxreborn): current={curr_morphe_hx} | upstream={latest_morphe_hx}")
    print(f"ReVanced Patches: current={curr_revanced} | upstream={latest_revanced}")

    if is_newer_version(latest_morphe_app, curr_morphe_app):
        print(f"==> NEW MORPHE YOUTUBE PATCH BUNDLE: {latest_morphe_app}! Queueing YouTube & YT Music rebuild...")
        updated_apps.update(['youtube', 'youtubemusic'])
        state['morphe_app_patches'] = latest_morphe_app

    if is_newer_version(latest_morphe_hx, curr_morphe_hx):
        print(f"==> NEW MORPHE MOVIEBOX PATCH BUNDLE: {latest_morphe_hx}! Queueing MovieBox rebuild...")
        updated_apps.add('moviebox')
        state['morphe_hx_patches'] = latest_morphe_hx

    if is_newer_version(latest_revanced, curr_revanced):
        print(f"==> NEW REVANCED PATCH BUNDLE: {latest_revanced}! Queueing Reddit rebuild...")
        updated_apps.add('reddit')
        state['revanced_patches'] = latest_revanced

    # 2. Check MovieBox official APK release
    print("\nChecking MovieBox official base APK...")
    mb_latest = get_moviebox_latest_version()
    mb_current = state.get('apps', {}).get('moviebox', '')
    print(f"MovieBox APK: current={mb_current} | upstream={mb_latest}")
    if is_newer_version(mb_latest, mb_current):
        print(f"==> NEW MOVIEBOX VERSION DETECTED: {mb_latest}")
        updated_apps.add('moviebox')
        state.setdefault('apps', {})['moviebox'] = mb_latest

    # 3. Check Flagship & Popular apps via Uptodown / Patch configs
    print("\nChecking flagship applications...")
    check_targets = {
        'youtube': 'https://youtube.en.uptodown.com/android',
        'youtubemusic': 'https://youtube-music.en.uptodown.com/android',
        'reddit': 'https://reddit-official-app.en.uptodown.com/android',
        'discord': 'https://discord-chat-for-gamers.en.uptodown.com/android',
        'duolingo': 'https://duolingo.en.uptodown.com/android',
        'tiktok': 'https://tiktok.en.uptodown.com/android',
        'instagram': 'https://instagram.en.uptodown.com/android',
        'twitter': 'https://twitter.en.uptodown.com/android',
        'bravebrowser': 'https://brave-browser.en.uptodown.com/android',
    }

    for app_id, url in check_targets.items():
        upstream_v = get_uptodown_version(url)
        current_v = state.get('apps', {}).get(app_id, '')
        if upstream_v:
            print(f"{app_id:15}: current={current_v:12} | upstream={upstream_v}")
            if is_newer_version(upstream_v, current_v):
                print(f"  ==> Upstream version updated for {app_id}: {current_v} -> {upstream_v}")
                if app_id in AUTONOMOUS_BUILD_APPS:
                    updated_apps.add(app_id)
                state['apps'][app_id] = upstream_v
        else:
            print(f"{app_id:15}: upstream check skipped (rate-limited/no-change)")

    save_state(state)

    buildable_apps = sorted([app for app in updated_apps if app in AUTONOMOUS_BUILD_APPS])

    print("\n==================================================")
    print(f"Update Check Finished. Apps requiring build: {buildable_apps}")
    print("==================================================")

    # 4. Trigger GitHub Actions if updates found and --trigger passed
    if buildable_apps and trigger_actions:
        print("Dispatching automated build via GitHub Actions...")
        try:
            if len(buildable_apps) > 1:
                print(f"Multiple apps updated ({buildable_apps}). Dispatching single consolidated 'all-flagships' workflow to save runner minutes...")
                cmd = ["gh", "workflow", "run", "build-and-release.yml", "-f", "target_app=all-flagships"]
                subprocess.run(cmd, check=True)
                print("Successfully dispatched consolidated all-flagships build.")
            else:
                target = buildable_apps[0]
                print(f"--> Triggering single build for: {target}")
                cmd = ["gh", "workflow", "run", "build-and-release.yml", "-f", f"target_app={target}"]
                subprocess.run(cmd, check=True)
                print(f"Successfully dispatched workflow for {target}")
        except Exception as e:
            print(f"Error dispatching workflow: {e}")
    elif buildable_apps:
        print("Run with '--trigger' to automatically launch GitHub Actions build for updated apps.")
    else:
        print("All apps and patch bundles are up to date! Zero builds needed.")

if __name__ == '__main__':
    main()
