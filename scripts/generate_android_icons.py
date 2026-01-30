#!/usr/bin/env python3
"""
Generate Android launcher icons (no white padding, no cropped edges).

Usage (from project root):
  python3 scripts/generate_android_icons.py path/to/logo.png
  python3 scripts/generate_android_icons.py path/to/logo.png --res android/app/src/main/res
  python3 scripts/generate_android_icons.py path/to/logo.png --bg "#5014C8"

Requires: pip install Pillow
"""

import argparse
import os
import sys

try:
    from PIL import Image
except ImportError:
    print("Install Pillow: pip install Pillow")
    sys.exit(1)


# Android density buckets: launcher/round size, foreground size, logo size in foreground (safe zone ~66%)
DENSITIES = {
    "mdpi": {"launcher": 48, "foreground": 108, "logo_in_fg": 72},
    "hdpi": {"launcher": 72, "foreground": 162, "logo_in_fg": 108},
    "xhdpi": {"launcher": 96, "foreground": 216, "logo_in_fg": 144},
    "xxhdpi": {"launcher": 144, "foreground": 324, "logo_in_fg": 216},
    "xxxhdpi": {"launcher": 192, "foreground": 432, "logo_in_fg": 288},
}


def hex_to_rgb(hex_color: str) -> tuple:
    h = hex_color.lstrip("#")
    if len(h) != 6:
        raise ValueError("Use 6-digit hex, e.g. #5014C8")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def main():
    parser = argparse.ArgumentParser(description="Generate Android launcher icons")
    parser.add_argument("logo", help="Path to square logo image (e.g. 1024x1024 PNG)")
    parser.add_argument(
        "--res",
        default="android/app/src/main/res",
        help="Path to android/app/src/main/res (default: android/app/src/main/res)",
    )
    parser.add_argument(
        "--bg",
        default="#5014C8",
        help="Background hex color for foreground safe zone (default: #5014C8)",
    )
    args = parser.parse_args()

    logo_path = os.path.abspath(args.logo)
    if not os.path.isfile(logo_path):
        print(f"Logo not found: {logo_path}")
        sys.exit(1)

    res_dir = os.path.abspath(args.res)
    if not os.path.isdir(res_dir):
        print(f"Res directory not found: {res_dir}")
        sys.exit(1)

    try:
        bg_rgb = hex_to_rgb(args.bg)
    except ValueError as e:
        print(e)
        sys.exit(1)

    logo = Image.open(logo_path).convert("RGBA")

    for density, dims in DENSITIES.items():
        mipmap_dir = os.path.join(res_dir, f"mipmap-{density}")
        os.makedirs(mipmap_dir, exist_ok=True)

        # 1. ic_launcher.png – full logo at launcher size
        launcher = logo.resize((dims["launcher"], dims["launcher"]), Image.Resampling.LANCZOS)
        launcher.save(os.path.join(mipmap_dir, "ic_launcher.png"), "PNG")

        # 2. ic_launcher_foreground.png – logo at safe zone size, centered on bg
        fg_size = dims["foreground"]
        logo_size = dims["logo_in_fg"]
        canvas = Image.new("RGBA", (fg_size, fg_size), bg_rgb + (255,))
        resized = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        offset = (fg_size - logo_size) // 2
        canvas.paste(resized, (offset, offset), resized)
        canvas.save(os.path.join(mipmap_dir, "ic_launcher_foreground.png"), "PNG")

        # 3. ic_launcher_round.png – same as launcher
        launcher.save(os.path.join(mipmap_dir, "ic_launcher_round.png"), "PNG")

        print(f"  mipmap-{density}: ic_launcher, ic_launcher_foreground, ic_launcher_round")

    print("\nDone. Next steps:")
    print("1. Ensure mipmap-anydpi-v26/ic_launcher.xml and ic_launcher_round.xml exist (see docs/ANDROID_LAUNCHER_ICONS.md).")
    print(f"2. Set ic_launcher_background in {res_dir}/values/ic_launcher_background.xml to {args.bg}.")
    print("3. cd android && ./gradlew clean && cd .. && npx react-native run-android")


if __name__ == "__main__":
    main()
