#!/usr/bin/env python3
# borealis_common.py — shared library for Borealis apps (theme engine core).
# Installed to /usr/lib/borealis/borealis_common.py by build.sh.

import json
import os
import re
import shutil
import subprocess
from pathlib import Path

HOME = Path.home()
SYSTEM_THEMES = Path("/usr/share/borealis/themes")
USER_THEMES = HOME / ".local/share/borealis/themes"
CURRENT_DIR = HOME / ".local/share/borealis/current"
STATE_DIR = HOME / ".config/borealis"
DEFAULT_WALLPAPER = "/usr/share/backgrounds/borealis/aurora-night.png"
THEME_STORE_URL_FILE = STATE_DIR / "theme-store-url"
DEFAULT_THEME_STORE_URL = (
    "https://raw.githubusercontent.com/borealis-linux/themes/main/index.json"
)


def run(cmd, **kw):
    """Run a command, return CompletedProcess (never raises)."""
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=kw.pop("timeout", 120), **kw)
    except Exception as e:  # noqa: BLE001 - UI code must not crash on subprocess issues
        class Fake:  # minimal stand-in
            returncode = 127
            stdout = ""
            stderr = str(e)
        return Fake()


def notify(title, body="", urgency="normal"):
    args = ["notify-send", "-u", urgency, title]
    if body:
        args.append(body)
    run(args)


def theme_dirs():
    """All available theme directories, user-installed taking precedence."""
    found = {}
    for base in (SYSTEM_THEMES, USER_THEMES):
        if base.is_dir():
            for d in sorted(base.iterdir()):
                if (d / "theme.json").is_file():
                    found[d.name] = d
    return found


def list_themes():
    out = []
    for name, d in theme_dirs().items():
        try:
            meta = json.loads((d / "theme.json").read_text())
            meta["dir"] = str(d)
            meta.setdefault("slug", name)
            out.append(meta)
        except Exception:
            continue
    return out


def current_theme_name():
    f = CURRENT_DIR / "theme-name"
    return f.read_text().strip() if f.is_file() else None


def _ensure_perf_variant(theme_dir: Path):
    """Guarantee an opaque dock stylesheet exists for Performance Mode."""
    perf = theme_dir / "waybar-perf.css"
    if perf.is_file():
        return
    css = (theme_dir / "waybar.css").read_text() if (theme_dir / "waybar.css").is_file() else ""
    # Collapse rgba(...) with alpha < 1 into solid rgb(...) — cheap to composite.
    def solidify(m):
        r, g, b, a = m.group(1), m.group(2), m.group(3), float(m.group(4))
        if a >= 0.99:
            return m.group(0)
        return f"rgb({r}, {g}, {b})"
    perf.write_text(re.sub(r"rgba\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*([\d.]+)\s*\)", solidify, css))


def apply_theme(slug: str) -> bool:
    """Apply a theme atomically: GTK css, dock style, wallpaper, icon set."""
    d = theme_dirs().get(slug)
    if not d:
        return False
    meta = json.loads((d / "theme.json").read_text())

    CURRENT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. GTK user stylesheet overlay
    gtk_dir = HOME / ".config/gtk-3.0"
    gtk_dir.mkdir(parents=True, exist_ok=True)
    if (d / "gtk.css").is_file():
        shutil.copyfile(d / "gtk.css", gtk_dir / "gtk.css")

    # 2. Dock styles (+ guaranteed perf variant)
    _ensure_perf_variant(d)
    for f in ("waybar.css", "waybar-perf.css"):
        if (d / f).is_file():
            shutil.copyfile(d / f, CURRENT_DIR / f)

    # 3. Wallpaper
    wall = meta.get("wallpaper", "wallpaper.png")
    if (d / wall).is_file():
        shutil.copyfile(d / wall, CURRENT_DIR / "wallpaper")

    # 4. GTK settings.ini (dark/light preference, fonts, icons)
    si = gtk_dir / "settings.ini"
    icon = meta.get("icons", "Papirus-Dark")
    cursor = meta.get("cursor", "Adwaita")
    font = meta.get("font", "Cantarell 11")
    dark = meta.get("variant", "dark") == "dark"
    si.write_text(
        "[Settings]\n"
        f"gtk-theme-name = {'Adwaita-dark' if dark else 'Adwaita'}\n"
        f"gtk-icon-theme-name = {icon}\n"
        f"gtk-font-name = {font}\n"
        f"gtk-cursor-theme-name = {cursor}\n"
        f"gtk-cursor-theme-size = 24\n"
        f"gtk-application-prefer-dark-theme = {'true' if dark else 'false'}\n"
        "gtk-enable-animations = true\n"
        "gtk-xft-antialias = 1\n"
        "gtk-xft-rgba = rgb\n"
        "gtk-xft-hintstyle = hintslight\n"
    )

    # 5. Shared schema keys (GTK4 apps, future tooling)
    run(["gsettings", "set", "org.gnome.desktop.interface", "color-scheme",
         "prefer-dark" if dark else "prefer-light"])
    run(["gsettings", "set", "org.gnome.desktop.interface", "icon-theme", icon])
    run(["gsettings", "set", "org.gnome.desktop.interface", "cursor-theme", cursor])

    # 6. Marker + live refresh of wallpaper & dock
    (CURRENT_DIR / "theme-name").write_text(meta.get("name", slug))
    run(["pkill", "-x", "swaybg"])
    os.system("setsid borealis-wallpaper >/dev/null 2>&1 &")
    run(["pkill", "-x", "waybar"])
    os.system("setsid borealis-bar >/dev/null 2>&1 &")
    return True


def perf_mode_enabled() -> bool:
    return (STATE_DIR / "perf-mode").is_file()


def boost_enabled() -> bool:
    runtime = os.environ.get("XDG_RUNTIME_DIR", "/tmp")
    f = Path(runtime) / "borealis-boost"
    return f.is_file() and f.read_text().strip() == "on"


def read_json(path, default=None):
    try:
        return json.loads(Path(path).read_text())
    except Exception:
        return default if default is not None else {}
