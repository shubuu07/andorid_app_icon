# andorid_app_icon

## Android launcher icon (no white padding / no cropped edges)

- **Guide:** [docs/ANDROID_LAUNCHER_ICONS.md](docs/ANDROID_LAUNCHER_ICONS.md) — copy to any app.
- **Regenerate icons:**  
  `python3 scripts/generate_android_icons.py path/to/logo.png`  
  Optional: `--res android/app/src/main/res` `--bg "#5014C8"`






Here’s what’s in place so you can reuse this for any app:
1. Guide – docs/ANDROID_LAUNCHER_ICONS.md
Why you get white padding and cropped edges.
What to add/fix: ic_launcher.xml, foreground safe zone (~66%), sizes per density.
Folder layout and a short “reuse in a new app” checklist.
Copy this file into any new project when you work on Android launcher icons.
2. Script – scripts/generate_android_icons.py
Usage (from project root):
  python3 scripts/generate_android_icons.py path/to/logo.png
Optional:
--res android/app/src/main/res (if your res folder is elsewhere)
--bg "#5014C8" (background color for the safe zone)
Requires: pip install Pillow
It generates ic_launcher.png, ic_launcher_foreground.png (with safe zone), and ic_launcher_round.png for all densities. Copy this script into a new app and run it with that app’s logo path.
