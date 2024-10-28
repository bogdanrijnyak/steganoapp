#!/bin/bash

# CryptoSafePDF Setup and Packaging Script for macOS

# 1. Install Homebrew (if not installed)
if ! command -v brew &>/dev/null; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "Homebrew already installed."
fi

# 2. Install create-dmg
if ! brew list create-dmg &>/dev/null; then
    echo "Installing create-dmg..."
    brew install create-dmg
else
    echo "create-dmg already installed."
fi

# 3. Install pyinstaller
if ! pip list | grep pyinstaller &>/dev/null; then
    echo "Installing pyinstaller..."
    pip install pyinstaller
else
    echo "pyinstaller already installed."
fi

# 4. Clean up previous builds
echo "Cleaning up previous builds..."
rm -rf build dist/*

# 5. Convert Python script to an application bundle
echo "Converting Python script to macOS app bundle..."
pyinstaller --name 'CryptoSafePDF' \
            --icon 'CryptoSafePDF.ico' \
            --windowed \
            --add-data='./strong_beat.wav:.' \
            --add-data='./sub_strong_beat.wav:.' \
            --add-data='./weak_beat.wav:.' \
            main.py

# 6. Create the DMG installer
echo "Creating DMG installer..."
mkdir -p dist/dmg
rm -rf dist/dmg/*
cp -r "dist/CryptoSafePDF.app" dist/dmg
create-dmg \
  --volname "CryptoSafePDF" \
  --volicon "CryptoSafePDF.ico" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "CryptoSafePDF.app" 175 120 \
  --hide-extension "CryptoSafePDF.app" \
  --app-drop-link 425 120 \
  "dist/CryptoSafePDF.dmg" \
  "dist/dmg/"

echo "Packaging complete. You can find the DMG installer in the dist/ directory."

