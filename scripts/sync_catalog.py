#!/usr/bin/env python3
"""
SDA Store - Catalog Sync Script
Scans GitHub Releases and updates data/apps.json with the latest verified APK assets.
"""

import os
import json
import argparse
import urllib.request
import datetime

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'apps.json')

def fetch_json(url):
    headers = {
        'User-Agent': 'SDA-Store-Catalog-Sync',
        'Accept': 'application/vnd.github.v3+json'
    }
    token = os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')
    if token:
        headers['Authorization'] = f'Bearer {token}'

    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as res:
        return json.loads(res.read().decode('utf-8'))

def sync_catalog(repo_name='sudarsanSDA/SDA-Store'):
    if not os.path.exists(DATA_PATH):
        print(f"Error: Catalog file not found at {DATA_PATH}")
        return

    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        catalog = json.load(f)

    print(f"Loaded catalog with {len(catalog.get('apps', []))} apps.")

    if not repo_name:
        print("No repository specified; maintaining existing asset URLs.")
        return

    print(f"Checking releases for repository: {repo_name}...")
    try:
        releases = fetch_json(f"https://api.github.com/repos/{repo_name}/releases")
        if not releases:
            print("No releases found on target repository.")
            return

        print(f"Retrieved {len(releases)} release(s). Processing assets...")
        updated_count = 0

        # Scan releases from newest to oldest
        for app in catalog.get('apps', []):
            app_id = app.get('id', '').lower()
            app_name_clean = app.get('name', '').lower().replace(' ', '')

            for release in releases[:10]:
                tag_name = release.get('tag_name', 'latest')
                release_url = release.get('html_url', '')
                matched_assets = []

                for asset in release.get('assets', []):
                    name = asset.get('name', '')
                    name_lower = name.lower()
                    if name_lower.endswith('.apk') and (app_id in name_lower or app_name_clean in name_lower):
                        arch = 'arm64' if 'arm64' in name_lower else ('arm' if ('arm-v7a' in name_lower or 'v7a' in name_lower) else 'universal')
                        matched_assets.append({
                            'name': name,
                            'arch': arch,
                            'version': tag_name.replace('release-', '').replace('v', ''),
                            'size': asset.get('size', 0),
                            'downloadUrl': asset.get('browser_download_url')
                        })

                if matched_assets:
                    app['assets'] = matched_assets
                    app['version'] = tag_name.replace('release-', '').replace('v', '')
                    app['releaseUrl'] = release_url
                    app['publishedAt'] = release.get('published_at', app.get('publishedAt'))
                    updated_count += 1
                    print(f"  -> Linked {len(matched_assets)} asset(s) for '{app.get('name')}' to {tag_name}")
                    break  # Found newest release for this app

        catalog['updatedAt'] = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

        with open(DATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(catalog, f, indent=2)

        print(f"Successfully synchronized {updated_count} app(s) in data/apps.json!")

    except Exception as e:
        print(f"Error syncing with GitHub API: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Synchronize SDA Store Catalog with GitHub Releases")
    parser.add_argument('--repo', type=str, default='sudarsanSDA/SDA-Store', help="GitHub repository in 'owner/repo' format")
    args = parser.parse_args()

    sync_catalog(args.repo)
