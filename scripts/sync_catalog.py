#!/usr/bin/env python3
"""
SDA Store - Catalog Sync Script
Scans GitHub Releases and updates data/apps.json with the latest verified APK assets.
"""

import os
import json
import argparse
import urllib.request

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'apps.json')

def fetch_json(url):
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'SDA-Store-Catalog-Sync'}
    )
    with urllib.request.urlopen(req, timeout=15) as res:
        return json.loads(res.read().decode('utf-8'))

def sync_catalog(repo_name=None):
    if not os.path.exists(DATA_PATH):
        print(f"Error: Catalog file not found at {DATA_PATH}")
        return

    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        catalog = json.load(f)

    print(f"Loaded catalog with {len(catalog.get('apps', []))} apps.")

    if not repo_name:
        print("No repository specified; maintaining existing verified asset URLs.")
        return

    print(f"Checking releases for repository: {repo_name}...")
    try:
        releases = fetch_json(f"https://api.github.com/repos/{repo_name}/releases")
        if not releases:
            print("No releases found on target repository.")
            return

        latest_release = releases[0]
        release_assets = latest_release.get('assets', [])
        print(f"Found {len(release_assets)} assets in release {latest_release.get('tag_name')}")

        updated_count = 0
        for app in catalog.get('apps', []):
            app_id = app.get('id')
            matched_assets = []
            for asset in release_assets:
                name = asset.get('name', '')
                if name.endswith('.apk') and (app_id in name.lower() or app['name'].lower().replace(' ', '') in name.lower()):
                    arch = 'arm64' if 'arm64' in name else ('arm' if 'arm-v7a' in name or 'v7a' in name else 'universal')
                    matched_assets.append({
                        'name': name,
                        'arch': arch,
                        'version': latest_release.get('tag_name', 'latest'),
                        'size': asset.get('size', 0),
                        'downloadUrl': asset.get('browser_download_url')
                    })

            if matched_assets:
                app['assets'] = matched_assets
                app['version'] = latest_release.get('tag_name', app.get('version'))
                app['releaseUrl'] = latest_release.get('html_url', app.get('releaseUrl'))
                updated_count += 1

        with open(DATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(catalog, f, indent=2)

        print(f"Successfully synchronized {updated_count} apps in data/apps.json!")

    except Exception as e:
        print(f"Error syncing with GitHub API: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Synchronize SDA Store Catalog with GitHub Releases")
    parser.add_argument('--repo', type=str, default='sudarsanSDA/SDA-Store', help="GitHub repository in 'owner/repo' format")
    args = parser.parse_args()

    sync_catalog(args.repo)
