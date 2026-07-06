#!/bin/bash
set -e

echo "=== Math Bot: environment setup ==="

# Android-specific variables
if [ -n "$TERMUX_VERSION" ]; then
    export CARGO_BUILD_TARGET=aarch64-linux-android
    export ANDROID_API_LEVEL=$(
        getprop ro.build.version.sdk 2>/dev/null || echo "34"
    )
    export ANDROID_NDK_HOME=/data/data/com.termux/files/usr
    echo "Termux: ANDROID_API_LEVEL=$ANDROID_API_LEVEL"
fi

# System packages (Termux only)
if [ -n "$TERMUX_VERSION" ]; then
    echo "Installing system packages..."
    pkg install -y python rust binutils cmake git 2>/dev/null
fi

# Virtual environment
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
fi
source .venv/bin/activate

# Python dependencies with caching
WHEELHOUSE="$HOME/.pip-wheels"
mkdir -p "$WHEELHOUSE"

if [ -f "requirements-lock.txt" ] && \
   [ "$(ls "$WHEELHOUSE"/*.whl 2>/dev/null)" ]; then
    echo "Installing from cache..."
    pip install --no-deps --find-links="$WHEELHOUSE" \
        -r requirements-lock.txt
else
    echo "Full install (first time)..."
    pip install -e ".[dev]"
    echo "Saving wheels to cache..."
    pip wheel -w "$WHEELHOUSE" -e ".[dev]"
    pip freeze > requirements-lock.txt
fi

echo "=== Done! Activate: source .venv/bin/activate ==="
