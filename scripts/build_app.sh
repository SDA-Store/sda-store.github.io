#!/usr/bin/env bash
set -e

# ==============================================================================
# SDA Store - Automated Headless APK Patcher
# Fetches base APKs from trusted sources, applies patches, and signs output APKs
# All builds and releases are hosted exclusively on sda-store/SDA-Store
# ==============================================================================

TARGET="${1:-moviebox}"
CUSTOM_URL="${2:-}"
BUILD_DIR="build_output"
WORKSPACE="workspace"
TOOLS_DIR="tools"

mkdir -p "$BUILD_DIR" "$WORKSPACE" "$TOOLS_DIR"

echo "========================================================"
echo "  SDA Store - Automated Headless APK Builder"
echo "  Target: $TARGET"
echo "========================================================"

# Setup ReVanced / RVX CLI & Patches
setup_tools() {
    echo "Checking RVX patcher tools..."

    if [ ! -f "$TOOLS_DIR/cli.jar" ]; then
        echo "Downloading inotia00/revanced-cli..."
        if command -v gh >/dev/null 2>&1; then
            gh release download --repo inotia00/revanced-cli --pattern "*all.jar" --output "$TOOLS_DIR/cli.jar" || true
        fi
        if [ ! -f "$TOOLS_DIR/cli.jar" ] || [ ! -s "$TOOLS_DIR/cli.jar" ]; then
            CLI_URL=$(curl -sL https://api.github.com/repos/inotia00/revanced-cli/releases/latest | grep -o 'https://[^"]*revanced-cli-[^"]*\.jar' | head -n 1)
            [ -z "$CLI_URL" ] && CLI_URL="https://github.com/inotia00/revanced-cli/releases/download/v5.0.2/revanced-cli-5.0.2-all.jar"
            curl -sL "$CLI_URL" -o "$TOOLS_DIR/cli.jar"
        fi
        echo "Downloaded CLI to $TOOLS_DIR/cli.jar"
    fi

    if [ ! -f "$TOOLS_DIR/patches.rvp" ]; then
        echo "Downloading inotia00/revanced-patches..."
        if command -v gh >/dev/null 2>&1; then
            gh release download --repo inotia00/revanced-patches --pattern "*.rvp" --output "$TOOLS_DIR/patches.rvp" || true
        fi
        if [ ! -f "$TOOLS_DIR/patches.rvp" ] || [ ! -s "$TOOLS_DIR/patches.rvp" ]; then
            PATCH_URL=$(curl -sL https://api.github.com/repos/inotia00/revanced-patches/releases/latest | grep -o 'https://[^"]*patches-[^"]*\.rvp' | head -n 1)
            [ -z "$PATCH_URL" ] && PATCH_URL="https://github.com/inotia00/revanced-patches/releases/download/v5.14.1/patches-5.14.1.rvp"
            curl -sL "$PATCH_URL" -o "$TOOLS_DIR/patches.rvp"
        fi
        echo "Downloaded Patches to $TOOLS_DIR/patches.rvp"
    fi
}

# Setup Morphe CLI & hxreborn Patches (engineered for MovieBox Ijiami unpacker)
setup_morphe_tools() {
    echo "Checking Morphe patcher tools for MovieBox..."

    if [ ! -f "$TOOLS_DIR/morphe-cli.jar" ]; then
        echo "Downloading Morphe Desktop CLI..."
        if command -v gh >/dev/null 2>&1; then
            gh release download --repo MorpheApp/morphe-desktop --pattern "*all.jar" --output "$TOOLS_DIR/morphe-cli.jar" || true
        fi
        if [ ! -f "$TOOLS_DIR/morphe-cli.jar" ] || [ ! -s "$TOOLS_DIR/morphe-cli.jar" ]; then
            CLI_URL=$(curl -sL https://api.github.com/repos/MorpheApp/morphe-desktop/releases/latest | grep -o 'https://[^"]*morphe-desktop-[^"]*\.jar' | head -n 1)
            [ -z "$CLI_URL" ] && CLI_URL="https://github.com/MorpheApp/morphe-desktop/releases/download/v1.18.1/morphe-desktop-1.18.1-all.jar"
            curl -sL "$CLI_URL" -o "$TOOLS_DIR/morphe-cli.jar"
        fi
        echo "Downloaded Morphe CLI to $TOOLS_DIR/morphe-cli.jar"
    fi

    if [ ! -f "$TOOLS_DIR/hxreborn-patches.mpp" ]; then
        echo "Downloading hxreborn/morphe-patches bundle..."
        if command -v gh >/dev/null 2>&1; then
            gh release download --repo hxreborn/morphe-patches --pattern "*.mpp" --output "$TOOLS_DIR/hxreborn-patches.mpp" || true
        fi
        if [ ! -f "$TOOLS_DIR/hxreborn-patches.mpp" ] || [ ! -s "$TOOLS_DIR/hxreborn-patches.mpp" ]; then
            PATCH_URL=$(curl -sL https://api.github.com/repos/hxreborn/morphe-patches/releases/latest | grep -o 'https://[^"]*patches-[^"]*\.mpp' | head -n 1)
            [ -z "$PATCH_URL" ] && PATCH_URL="https://github.com/hxreborn/morphe-patches/releases/download/v1.55.0/patches-1.55.0.mpp"
            curl -sL "$PATCH_URL" -o "$TOOLS_DIR/hxreborn-patches.mpp"
        fi
        echo "Downloaded hxreborn patches to $TOOLS_DIR/hxreborn-patches.mpp"
    fi
}

# Fetch base APK from trusted source if not already in workspace
fetch_base_apk() {
    local app="$1"
    local base_path="$WORKSPACE/base-${app}.apk"

    if [ -f "$base_path" ] && [ -s "$base_path" ]; then
        echo "Base APK '$base_path' already exists in workspace."
        return 0
    fi

    if [ -n "$CUSTOM_URL" ]; then
        echo "Downloading base APK from provided custom URL: $CUSTOM_URL"
        curl -sL -A "Mozilla/5.0 (Android; Mobile; rv:130.0) Gecko/130.0 Firefox/130.0" "$CUSTOM_URL" -o "$base_path"
        return 0
    fi

    echo "Fetching base APK for '$app'..."

    if [ "$app" = "moviebox" ]; then
        echo "Fetching official MovieBox base APK from movie-box.co..."
        MOVIEBOX_OFFICIAL_URL="https://h5-api.aoneroom.com/pkg/redirect"
        curl -sL -f -A "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36" \
            "$MOVIEBOX_OFFICIAL_URL" -o "$base_path" || true
        
        if [ ! -f "$base_path" ] || [ ! -s "$base_path" ] || [ $(wc -c < "$base_path" 2>/dev/null || echo 0) -lt 10000000 ]; then
            echo "Fallback to direct CDN release URL for MovieBox..."
            curl -sL -f -A "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36" \
                "https://apk.aoneroom.com/apk/moviebox/release/4.0.03.0922.03/1218_protected_signed/moviebox-in-v-4.0.03.0922.03.apk" -o "$base_path"
        fi
        return 0
    fi

    # Lookup in data/patches/ TOML configs
    local toml_file="data/patches/${app}.toml"
    if [ ! -f "$toml_file" ]; then
        toml_file=$(ls data/patches/*${app}*.toml 2>/dev/null | head -n 1 || true)
    fi

    if [ -f "$toml_file" ]; then
        echo "Found patch configuration in $toml_file"
        local uptodown_url=$(grep -E '^\s*uptodown-dlurl\s*=' "$toml_file" | head -n 1 | cut -d'"' -f2 || true)
        local archive_url=$(grep -E '^\s*archive-dlurl\s*=' "$toml_file" | head -n 1 | cut -d'"' -f2 || true)

        if [ -n "$uptodown_url" ]; then
            echo "Attempting to resolve & download base APK via Uptodown ($uptodown_url)..."
            if python3 scripts/uptodown.py download "$uptodown_url" "" "$base_path" "arm64-v8a" 2>/dev/null; then
                echo "Successfully downloaded base APK via Uptodown!"
                return 0
            fi
        fi

        if [ ! -f "$base_path" ] || [ ! -s "$base_path" ]; then
            if [ -n "$archive_url" ]; then
                echo "Attempting direct download from archive mirror ($archive_url)..."
                curl -sL -A "Mozilla/5.0" "$archive_url" -o "$base_path" || true
            fi
        fi
    fi

    if [ ! -f "$base_path" ] || [ ! -s "$base_path" ]; then
        echo "Notice: Base APK for '$app' could not be downloaded automatically."
        echo "Please place clean '$base_path' into workspace/ or specify custom_apk_url in workflow dispatch."
        return 1
    fi
}

# Patch and sign single app
patch_app() {
    local app="$1"
    local base_apk="$WORKSPACE/base-${app}.apk"
    local output_apk="$BUILD_DIR/${app}-patched-arm64-v8a.apk"

    fetch_base_apk "$app" || return 1

    echo "Applying patches to $base_apk..."
    if [ "$app" = "moviebox" ]; then
        setup_morphe_tools
        echo "Patching MovieBox using Morphe CLI & hxreborn patches..."
        java -jar "$TOOLS_DIR/morphe-cli.jar" patch \
            -p "$TOOLS_DIR/hxreborn-patches.mpp" \
            -f \
            -o "$output_apk" \
            "$base_apk"
    else
        setup_tools
        echo "Patching $app using RVX CLI..."
        if [ -f "$TOOLS_DIR/cli.jar" ] && [ -f "$TOOLS_DIR/patches.rvp" ]; then
            java -jar "$TOOLS_DIR/cli.jar" patch \
                -p "$TOOLS_DIR/patches.rvp" \
                -f \
                --purge \
                --signer "SDA Store" \
                -o "$output_apk" \
                "$base_apk"
        else
            echo "Error: CLI ($TOOLS_DIR/cli.jar) or patches bundle ($TOOLS_DIR/patches.rvp) missing."
            return 1
        fi
    fi

    echo ">>> SUCCESS: Built and signed: $output_apk"
}

case "$TARGET" in
    moviebox)
        patch_app "moviebox"
        ;;
    youtube)
        patch_app "youtube"
        ;;
    youtubemusic|youtube-music)
        patch_app "youtube-music"
        ;;
    reddit)
        patch_app "reddit"
        ;;
    twitter)
        patch_app "twitter"
        ;;
    instagram)
        patch_app "instagram"
        ;;
    tiktok)
        patch_app "tiktok"
        ;;
    bravebrowser|brave)
        patch_app "brave"
        ;;
    duolingo)
        patch_app "duolingo"
        ;;
    discord)
        patch_app "discord"
        ;;
    photos)
        patch_app "photos"
        ;;
    all|all-flagships)
        echo "Building flagship apps suite..."
        for a in moviebox youtube reddit twitter instagram tiktok brave; do
            echo "--- Starting patch for $a ---"
            patch_app "$a" || true
        done
        ;;
    all-apps)
        echo "Building all configured apps in data/patches/..."
        for f in data/patches/*.toml; do
            app_slug=$(basename "$f" .toml)
            echo "--- Starting patch for $app_slug ---"
            patch_app "$app_slug" || true
        done
        ;;
    *)
        patch_app "$TARGET"
        ;;
esac

echo "========================================================"
echo "Build complete. Output files in $BUILD_DIR:"
ls -lh "$BUILD_DIR" || true
echo "========================================================"
