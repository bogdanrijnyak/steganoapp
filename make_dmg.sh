#!/bin/sh

# Clean up previous builds
echo "Cleaning up previous builds..."
rm -rf build dist/*

# Step 1: Convert Python script to an application bundle
echo "Converting Python script to macOS app bundle..."
pyinstaller --name 'Steganographer' --windowed --onefile --icon 'Steganographer.icns' --hidden-import 'tkinter' --hidden-import 'pillow' --hidden-import 'os' --hidden-import 'PIL' newscript.py

# Verify the build
if [ ! -d "dist/Steganographer.app" ]; then
  echo "Error: Application bundle was not created. Please check your script for errors."
  exit 1
fi

# Step 2: Create the DMG installer
echo "Creating DMG installer..."

mkdir -p dist/dmg
rm -rf dist/dmg/*
cp -r "dist/Steganographer.app" dist/dmg/

create-dmg \
  --volname "Steganographer" \
  --app-drop-link 425 120 \
  "dist/Steganographer.dmg" \
  "dist/dmg/"

echo "Packaging complete. You can find the DMG installer in the dist/ directory."
