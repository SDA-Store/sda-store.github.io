#!/usr/bin/env bash
set -e

# ==============================================================================
# SDA Store - Automated Headless APK Patcher
# Fetches base APKs from trusted sources, applies patches, and signs output APKs
# ==============================================================================

TARGET="${1:-moviebox}"
CUSTOM_URL="${2:-}"
BUILD_DIR="build_output"
WORKSPACE="workspace"
TOOLS_DIR="tools"

mkdir -p "$BUILD_DIR" "$WORKSPACE" "$TOOLS_DIR"

echo "========================================================"
echo "  SDA Store - Headless APK Builder"
echo "  Target: $TARGET"
echo "========================================================"

# Setup CLI & Patches if not present
setup_tools() {
    echo "Checking patcher tools..."

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

    echo "Fetching base APK for '$app' from verified source..."

    case "$app" in
        moviebox)
            # Official MovieBox redirector & CDN from movie-box.co
            echo "Fetching official MovieBox base APK from movie-box.co..."
            MOVIEBOX_OFFICIAL_URL="https://h5-api.aoneroom.com/pkg/redirect"
            curl -sL -f -A "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36" \
                "$MOVIEBOX_OFFICIAL_URL" -o "$base_path" || true
            
            # Verify file size > 10MB or fallback to direct CDN release URL
            if [ ! -f "$base_path" ] || [ ! -s "$base_path" ] || [ $(wc -c < "$base_path" 2>/dev/null || echo 0) -lt 10000000 ]; then
                echo "Fallback to direct CDN release URL for MovieBox..."
                curl -sL -f -A "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36" \
                    "https://apk.aoneroom.com/apk/moviebox/release/4.0.03.0922.03/1218_protected_signed/moviebox-in-v-4.0.03.0922.03.apk" -o "$base_path"
            fi
            ;;
        youtube)
            echo "Fetching YouTube base APK..."
            # Handled in GitHub Actions via gh-apkmirror-dl or custom URL
            ;;
        reddit)
            echo "Fetching Reddit base APK..."
            # Handled in GitHub Actions via gh-apkmirror-dl or custom URL
            ;;
        *)
            echo "Unknown app for auto-fetch: $app"
            ;;
    esac

    if [ ! -f "$base_path" ] || [ ! -s "$base_path" ]; then
        echo "Notice: Base APK for $app could not be downloaded automatically."
        echo "Please place clean '$base_path' into the workspace/ directory or supply a direct download URL."
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
    if [ -f "$TOOLS_DIR/cli.jar" ] && [ -f "$TOOLS_DIR/patches.rvp" ]; then
        java -jar "$TOOLS_DIR/cli.jar" patch \
            -p "$TOOLS_DIR/patches.rvp" \
            -f \
            --purge \
            --signer "SDA Store" \
            -o "$output_apk" \
            "$base_apk"

        echo ">>> SUCCESS: Built and signed: $output_apk"
    else
        echo "Error: CLI ($TOOLS_DIR/cli.jar) or patches bundle ($TOOLS_DIR/patches.rvp) missing."
        return 1
    fi
}

setup_tools

case "$TARGET" in
    moviebox)
        patch_app "moviebox"
        ;;
    youtube)
        patch_app "youtube"
        ;;
    reddit)
        patch_app "reddit"
        ;;
    all)
        echo "Building all configured apps..."
        for a in moviebox youtube reddit; do
            patch_app "$a" || true
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
