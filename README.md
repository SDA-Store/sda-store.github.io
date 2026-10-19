# SDA Store 📱✨
> **Fast, Modern Catalog for Patched Android APKs**  
> *100% Non-Root APKs. Zero Modules. Automated GitHub Actions CI/CD.*

[![Automated APK Builder & Release](https://github.com/sudarsanSDA/SDA-Store/actions/workflows/build-and-release.yml/badge.svg)](https://github.com/sudarsanSDA/SDA-Store/actions/workflows/build-and-release.yml)
[![Upstream Update Watcher](https://github.com/sudarsanSDA/SDA-Store/actions/workflows/auto-update-watcher.yml/badge.svg)](https://github.com/sudarsanSDA/SDA-Store/actions/workflows/auto-update-watcher.yml)
[![Deploy SDA Store to GitHub Pages](https://github.com/sudarsanSDA/SDA-Store/actions/workflows/deploy-pages.yml/badge.svg)](https://github.com/sudarsanSDA/SDA-Store/actions/workflows/deploy-pages.yml)
[![Latest Release](https://img.shields.io/github/v/release/sudarsanSDA/SDA-Store?style=flat&color=10b981)](https://github.com/sudarsanSDA/SDA-Store/releases)

---

## 🌟 Overview

**SDA Store** is an open-source, automated Android application catalog designed to make discovering, installing, and updating patched Android apps effortless:
* **136+ Patched Applications:** Complete replicated catalog with real local icons, applied patch details, and direct APK download binaries.
* **APKs Only:** Filtered strictly for standalone, non-root `.apk` binaries (no Magisk/KernelSU modules).
* **Automated Builds & Releases:** Production-grade GitHub Actions CI/CD pipeline that downloads base APKs via Uptodown/APKMirror, applies patches via Morphe CLI and ReVanced CLI, signs with keystore, and publishes directly to GitHub Releases.
* **Obtainium Integration:** One-click install and background auto-updates through [Obtainium](https://github.com/ImranR98/Obtainium).
* **Zero Cost:** Hosted entirely on **GitHub Pages** and **GitHub Actions**.

---

## 🚀 Curated Apps Included

| App | Framework / Brand | Top Features | Architecture |
|---|---|---|---|
| **YouTube** | Morphe / ReVanced | Ad-free, Background Play, SponsorBlock, Return Dislike, AMOLED | ARM64, ARM-v7a |
| **YouTube Music** | Morphe | Ad-free audio stream, Background play, Audio-only mode | ARM64, ARM-v7a |
| **Reddit** | Morphe | Promoted posts removed, Gallery downloader, AMOLED Black | ARM64, ARM-v7a |
| **Instagram** | HushGram | Feed & Reel ads blocked, Download stories/reels, Ghost mode | ARM64 |
| **Twitter / X** | Piko | Timeline ads stripped, Telemetry blocked, Media downloader | ARM64, ARM-v7a |
| **Google Photos** | AkashSriram | Pixel Exclusive Features unlocked, Unlimited backup spoofing | ARM64, ARM-v7a |
| **Brave Browser** | Origin | Telemetry & ad tracking removed, Startup optimizations | ARM64, ARM-v7a |
| **TikTok** | HushFeed | No watermarks, Ad-free feed, Region lock bypass, Pure black | ARM64, ARM-v7a |
| **Duolingo** | Hoodles | Heart limit bypass, Unlimited practice, Ad-free | ARM64, ARM-v7a |
| **ReVanced GmsCore** | ReVanced | Essential MicroG helper for Google login on non-root | Universal |

---

## 🛠️ Project Structure

```text
d:/SDA Store/
├── index.html                   # Main storefront application
├── css/
│   └── style.css                # Modern design system (tokens, glassmorphism, responsive)
├── js/
│   └── app.js                   # Reactive app logic, search, filters & Obtainium integration
├── data/
│   └── apps.json                # Structured catalog feed (APKs, patch sets, versions)
├── .github/
│   └── workflows/
│       ├── deploy-pages.yml     # Automated GitHub Pages deployment
│       └── build-and-release.yml# Headless APK patching & release pipeline
├── scripts/
│   ├── build_app.sh             # Headless CLI patcher script
│   └── sync_catalog.py          # Python sync tool to update data/apps.json from GitHub API
└── README.md                    # Project documentation
```

---

## 🌐 Deploy to GitHub Pages (100% Free)

You can host this entire store on GitHub Pages in under 2 minutes:

1. **Initialize & Push your files:**
   ```bash
   git init
   git add .
   git commit -m "feat: initial SDA Store release"
   git branch -M main
   git remote add origin https://github.com/sudarsanSDA/SDA-Store.git
   git push -u origin main
   ```
2. **Enable GitHub Pages:**
   * Go to your repository **Settings** &rarr; **Pages**.
   * Under **Build and deployment &rarr; Source**, choose **GitHub Actions**.
3. **Access your site:**
   * Your store will be live at `https://sudarsansda.github.io/SDA-Store/`.

---

## ⚡ Automated APK Builder & Patching Pipeline (GitHub Actions)

The repository includes a complete, production-grade headless build automation system powered by GitHub Actions ([`.github/workflows/build-and-release.yml`](.github/workflows/build-and-release.yml)):

* **Direct Pipeline Link:** [https://github.com/sudarsanSDA/SDA-Store/actions](https://github.com/sudarsanSDA/SDA-Store/actions)
* **Automated Daily Runs:** Configured on cron schedule (`0 2 * * *`) to automatically pull the newest clean base APKs and re-apply latest upstream patches daily.
* **Supported Build Targets:**
  * `all-flagships`: Batch builds all high-priority flagships (MovieBox, YouTube, Reddit, Twitter, Instagram, TikTok, Brave).
  * `all-apps`: Iterates through all 57 patch configurations in `data/patches/`.
  * Individual apps: `moviebox`, `youtube`, `youtubemusic`, `reddit`, `twitter`, `instagram`, `tiktok`, `bravebrowser`, `duolingo`, `discord`, `photos`, etc.
  * Custom base APKs: Pass any clean APK direct URL via `custom_apk_url`.

### How to Trigger a Build in GitHub Actions:
1. Navigate to the **[Actions Tab](https://github.com/sudarsanSDA/SDA-Store/actions)**.
2. Select **[Automated APK Builder & Release](https://github.com/sudarsanSDA/SDA-Store/actions/workflows/build-and-release.yml)** from the left sidebar.
3. Click the **Run workflow** dropdown on the right.
4. Choose your desired target (`all-flagships`, `moviebox`, `youtube`, etc.) and click the green **Run workflow** button.
5. GitHub Actions executes:
   - Downloads official base APKs via direct CDN / Uptodown / APKMirror.
   - Executes bytecode transformation and unhardening via Morphe CLI (`.mpp`) or ReVanced CLI (`.rvp`).
   - Signs the APK with Android `apksigner`.
   - Uploads the signed `.apk` as a 14-day CI artifact (instant download from workflow summary).
   - Publishes a formal release to [GitHub Releases](https://github.com/sudarsanSDA/SDA-Store/releases).
   - Syncs `data/apps.json` with the new download link and triggers the live GitHub Pages redeployment.

---

## 🤖 Autonomous Upstream Update Watcher & Auto-Builds

In addition to manual triggers and daily runs, the repository includes an automated update watcher ([`.github/workflows/auto-update-watcher.yml`](.github/workflows/auto-update-watcher.yml)):

* **Runs Every 6 Hours:** Automatically queries upstream repositories for new releases:
  * **Base APKs:** Monitors upstream APK releases (YouTube, Reddit, Discord, Duolingo, TikTok, MovieBox, etc.) via Uptodown / APKMirror / official CDNs.
  * **Patch Bundles:** Monitors new patch bundle releases for Morphe (`hxreborn/morphe-patches`) and ReVanced (`inotia00/revanced-patches`).
* **Auto-Dispatch:** If a new APK or patch version is detected, the watcher records the new version in `data/upstream_state.json` and automatically triggers `build-and-release.yml` for the updated application.
* **Autonomous Release & Publish:** The builder compiles the updated APK, signs it with Android `apksigner`, publishes a new release on GitHub Releases, updates `data/apps.json`, and redeploys the GitHub Pages store without any manual intervention!

---

## 📲 Obtainium Auto-Update Setup

Users don't have to keep redownloading APKs manually:
1. Install [Obtainium](https://github.com/ImranR98/Obtainium/releases/latest) on your Android device.
2. Open **SDA Store** on your phone.
3. Tap **Obtainium** on any app card.
4. Obtainium opens with the repository URL and APK filter pre-configured. Tap **Add** &mdash; Obtainium will now notify and auto-update your apps whenever a new release is published!

---

## ⚖️ Legal & Best Practices Note
* Distributing pre-patched proprietary applications publicly carries DMCA risk from copyright holders.
* For long-term sustainability, consider keeping automated APK builder repositories **Private** for your personal devices, or use the client-side patching flow (Morphe Manager) for public audiences.
