# Android Launcher Icon Guide (Any App)

Use this when your Android app icon has **white padding** or **cropped edges** on the home screen.

---

## Why it happens

1. **White padding**
   - Missing `ic_launcher.xml` in `mipmap-anydpi-v26/`, so Android falls back to old PNGs that may have white/extra padding.
   - Or the foreground image was drawn with extra margin.

2. **Logo cutting at edges**
   - Android **adaptive icons** (API 26+) crop about **18% from each edge** (“safe zone”).
   - If the logo fills the whole foreground image, the edges get cut off.

---

## Fix in 3 steps

### 1. Add adaptive icon XML (fixes white padding)

Ensure both files exist in `android/app/src/main/res/mipmap-anydpi-v26/`:

**`ic_launcher.xml`** (often missing):

```xml
<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/ic_launcher_background"/>
    <foreground android:drawable="@mipmap/ic_launcher_foreground"/>
</adaptive-icon>
```

**`ic_launcher_round.xml`** – same content as above.

Background color is in `res/values/ic_launcher_background.xml` (e.g. `#5014C8`). Match it to your logo.

---

### 2. Foreground image = logo inside safe zone (fixes cropped edges)

- **Foreground size** (per density): 108dp → 432px at xxxhdpi, etc.
- **Safe zone**: only the center **~66%** is guaranteed visible.
- So: **scale the logo to ~66% of the foreground canvas and center it**; use your brand color for the rest of the canvas.

| Density  | Canvas (px) | Logo size (px) |
|----------|-------------|----------------|
| mdpi     | 108         | 72             |
| hdpi     | 162         | 108            |
| xhdpi    | 216         | 144            |
| xxhdpi   | 324         | 216            |
| xxxhdpi  | 432         | 288            |

---

### 3. Launcher and round icons (legacy / non-adaptive)

Use the **full logo** (no safe zone), one size per density:

| Density  | Size (px) |
|----------|-----------|
| mdpi     | 48        |
| hdpi     | 72        |
| xhdpi    | 96        |
| xxhdpi   | 144       |
| xxxhdpi  | 192       |

Same for `ic_launcher.png` and `ic_launcher_round.png`.

---

## Quick reference: folder structure

```
android/app/src/main/res/
├── mipmap-anydpi-v26/
│   ├── ic_launcher.xml          ← adaptive (square)
│   └── ic_launcher_round.xml    ← adaptive (round)
├── mipmap-mdpi/   ... xxxhdpi/
│   ├── ic_launcher.png
│   ├── ic_launcher_foreground.png   ← logo at ~66%, centered
│   └── ic_launcher_round.png
└── values/
    └── ic_launcher_background.xml   ← hex color
```

---

## Reusing in a new app

1. Copy this guide (or the `scripts/generate_android_icons.py` script) into the new project.
2. Run the script with your logo path and Android `res` path (see script usage).
3. Set `ic_launcher_background` in `values/` to match your logo.
4. Ensure `ic_launcher.xml` and `ic_launcher_round.xml` exist in `mipmap-anydpi-v26/`.
5. Clean and rebuild: `cd android && ./gradlew clean && cd .. && npx react-native run-android`.

---

## After changing icons

- Rebuild and reinstall the app.
- If the launcher still shows the old icon: uninstall the app and install again, or clear the launcher’s cache.
