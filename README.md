# SDA Store 📱✨
> **Fast, Modern Catalog for Patched Android APKs**  
> *Inspired by NullStore & Morphe Patches. 100% Non-Root APKs. Zero Modules. Free GitHub Hosting.*

---

## 🌟 Overview

**SDA Store** is an open-source, automated Android application catalog designed to make discovering, installing, and updating patched Android apps effortless:
* **APKs Only:** Filtered strictly for standalone, non-root `.apk` binaries (no Magisk/KernelSU modules).
* **Automated Builds & Releases:** Ready-to-use GitHub Actions workflows that apply patches via CLI and upload to GitHub Releases.
* **Obtainium Integration:** One-click install and background auto-updates through [Obtainium](https://github.com/ImranR98/Obtainium).
* **Zero Cost:** Hosted entirely for free on **GitHub Pages** with zero domain, server, or storage fees.

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

## ⚡ How the Automated APK Builder Works

The repository includes a complete GitHub Actions CI/CD workflow (`.github/workflows/build-and-release.yml`):

1. **Matrix / Manual Trigger:**
   * Trigger builds on a weekly cron schedule or manually choose which app to patch via `workflow_dispatch`.
2. **Headless Patching:**
   * Runs Java 21 on `ubuntu-latest`.
   * Automatically downloads the latest CLI patcher and `.mpp` / `.jar` patch bundles.
   * Applies smali/dex transformations and resource rebuilding.
3. **Auto-Signing:**
   * Generates a persistent release keystore and signs with Android's `apksigner`.
4. **Automated GitHub Releases:**
   * Publishes the compiled `.apk` files directly to GitHub Releases.
5. **Catalog Sync:**
   * Runs `scripts/sync_catalog.py` to automatically update `data/apps.json` with the new release URLs and commit back to `main`.

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
