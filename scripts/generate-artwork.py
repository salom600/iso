#!/usr/bin/env python3
"""generate-artwork.py — reproducible artwork for Borealis Linux.

Generates (deterministically, seed=42):
  * wallpapers:   aurora-night.png (dark, anime-inspired), glacier-light.png
  * theme assets: themes/<slug>/wallpaper.png for each shipped theme
  * branding:     calamares/borealis/branding/logo.png
  * out-of-box:   /etc/skel/.local/share/borealis/current/* (Aurora Night)
                  + skel gtk.css so first boot is already themed

Run by build.sh with --root <repo>. Needs python3-pil on the build host.
"""

import argparse
import random
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

SEED = 42
W, H = 1920, 1080


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def gradient(w, h, stops):
    """Vertical multi-stop gradient."""
    img = Image.new("RGB", (w, h))
    dr = ImageDraw.Draw(img)
    n = len(stops) - 1
    for y in range(h):
        t = y / max(1, h - 1)
        seg = min(int(t * n), n - 1)
        local = (t - seg / n) * n
        c = lerp(stops[seg], stops[seg + 1], local)
        dr.line([(0, y), (w, y)], fill=c)
    return img


def add_glow(layer, color, center, radius, alpha):
    d = ImageDraw.Draw(layer, "RGBA")
    x, y = center
    d.ellipse([x - radius, y - radius, x + radius, y + radius],
              fill=color + (alpha,))
    return layer.filter(ImageFilter.GaussianBlur(radius // 2))


def aurora_night():
    rng = random.Random(SEED)
    img = gradient(W, H, [(9, 13, 26), (16, 22, 44), (13, 18, 36), (6, 9, 20)])
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    # moon + halo
    add_glow(glow, (200, 220, 255), (int(W * 0.78), int(H * 0.20)), 210, 46)
    d = ImageDraw.Draw(glow, "RGBA")
    mx, my, mr = int(W * 0.78), int(H * 0.20), 74
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(236, 243, 255, 255))
    d.ellipse([mx - 20, my - 26, mx - 6, my - 12], fill=(206, 218, 240, 90))

    # aurora ribbons (teal/violet), drawn as thick translucent curves + blur
    for i, (hue, x0, y0) in enumerate((
            ((94, 226, 200), 0.10, 0.42), ((128, 160, 255), 0.30, 0.30),
            ((186, 132, 252), 0.52, 0.46), ((94, 226, 255), 0.70, 0.34))):
        pts = []
        for k in range(-40, 41):
            x = int(W * (x0 + k * 0.016))
            y = int(H * (y0 + rng.uniform(-0.05, 0.05) + 0.06 * ((k / 40) ** 2)))
            pts.append((x, y))
        ribbon = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        rd = ImageDraw.Draw(ribbon, "RGBA")
        for t in range(3):
            width = 90 - t * 26
            rd.line([(px, py + t * 14) for px, py in pts],
                    fill=hue + (58 - t * 16,), width=width, joint="curve")
        ribbon = ribbon.filter(ImageFilter.GaussianBlur(34))
        glow.alpha_composite(ribbon)

    # stars
    d = ImageDraw.Draw(glow, "RGBA")
    for _ in range(420):
        x, y = rng.randrange(W), rng.randrange(int(H * 0.75))
        r = rng.choice((1, 1, 1, 2))
        a = rng.randrange(60, 220)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, a))
    img = Image.alpha_composite(img.convert("RGBA"), glow)

    # mountain silhouettes (two ridges)
    d = ImageDraw.Draw(img, "RGBA")
    for depth, (base_y, alpha, col) in enumerate((
            (0.80, 235, (11, 16, 30)), (0.88, 255, (6, 9, 19)))):
        pts = [(0, H)]
        x = 0
        rng2 = random.Random(SEED + depth)
        while x < W:
            peak = base_y + rng2.uniform(-0.16, 0.02)
            pts += [(x, int(H * peak)), (x + W // 26, int(H * (base_y + rng2.uniform(-0.02, 0.10))))]
            x += W // 13
        pts += [(W, H)]
        d.polygon(pts, fill=col + (alpha,))

    # sakura petals drifting (anime touch)
    for _ in range(46):
        s = rng.uniform(4, 9)
        petal = Image.new("RGBA", (int(s * 3), int(s * 3)), (0, 0, 0, 0))
        pd = ImageDraw.Draw(petal)
        pd.ellipse([s * 0.6, s * 0.2, s * 2.2, s * 1.7],
                   fill=(255, (183 + int(rng.uniform(-20, 20)) % 255), 208, 150))
        petal = petal.rotate(rng.uniform(0, 360), expand=True)
        x = rng.randrange(0, max(1, W - petal.width))
        y = rng.randrange(0, max(1, int(H * 0.85) - petal.height))
        img.alpha_composite(petal, (int(x), int(y)))

    return img.convert("RGB")


def glacier_light():
    rng = random.Random(SEED + 7)
    img = gradient(W, H, [(238, 244, 252), (218, 232, 248), (196, 218, 244), (170, 200, 236)])
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    # sun glow
    add_glow(layer, (255, 250, 230), (int(W * 0.72), int(H * 0.24)), 260, 120)

    # translucent ice polygons
    d = ImageDraw.Draw(layer, "RGBA")
    for _ in range(14):
        cx, cy = rng.randrange(W), rng.randrange(int(H * 0.55), int(H * 0.95))
        r = rng.uniform(60, 220)
        pts = [(cx + r * rng.uniform(-1, 1), cy + r * rng.uniform(-1, 1)) for _ in range(3)]
        d.polygon(pts, fill=(255, 255, 255, rng.randrange(22, 60)),
                  outline=(255, 255, 255, 90))
    layer = layer.filter(ImageFilter.GaussianBlur(2))

    # accent diamond
    d = ImageDraw.Draw(layer, "RGBA")
    cx, cy, r = int(W * 0.5), int(H * 0.42), 56
    d.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)],
              fill=(10, 124, 196, 200))
    img = Image.alpha_composite(img.convert("RGBA"), layer)

    # soft horizon line
    d = ImageDraw.Draw(img, "RGBA")
    d.line([(0, int(H * 0.86)), (W, int(H * 0.90))], fill=(120, 160, 210, 140), width=3)
    return img.convert("RGB")


def logo(size=256):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    g = Image.new("RGB", (size, size))
    dg = ImageDraw.Draw(g)
    for y in range(size):
        dg.line([(0, y), (size, y)],
                fill=lerp((56, 168, 255), (150, 92, 255), y / size))
    mask = Image.new("L", (size, size), 0)
    dm = ImageDraw.Draw(mask)
    dm.rounded_rectangle([4, 4, size - 4, size - 4], radius=size // 5, fill=255)
    img.paste(g, (0, 0), mask)
    d = ImageDraw.Draw(img)
    cx = cy = size // 2
    r = size // 4
    d.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)],
              fill=(255, 255, 255, 245))
    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="repository root")
    args = ap.parse_args()
    root = Path(args.root)

    bgs = root / "config/includes.chroot/usr/share/backgrounds/borealis"
    bgs.mkdir(parents=True, exist_ok=True)

    art = {"aurora-night": aurora_night(), "glacier-light": glacier_light()}
    for name, im in art.items():
        im.save(bgs / f"{name}.png", optimize=True)
        print(f"wallpaper: {name}.png")

    # theme wallpapers (themes carry their own copy for the pack format)
    for slug, name in (("aurora-night", "aurora-night"), ("glacier-light", "glacier-light")):
        tdir = root / "themes" / slug
        if tdir.is_dir():
            art[name].save(tdir / "wallpaper.png", optimize=True)
            print(f"theme wallpaper: {slug}/wallpaper.png")

    # branding logo
    logo_dir = root / "calamares/branding"
    logo_dir.mkdir(parents=True, exist_ok=True)
    logo().save(logo_dir / "logo.png")
    logo(64).save(root / "config/includes.chroot/usr/share/icons/borealis-logo.png")
    print("logo: calamares branding + icon")

    # Out-of-box theme wiring: first boot boots into Aurora Night.
    skel_current = root / "config/includes.chroot/etc/skel/.local/share/borealis/current"
    skel_current.mkdir(parents=True, exist_ok=True)
    aur = root / "themes/aurora-night"
    if aur.is_dir():
        for f in ("waybar.css", "gtk.css"):
            src = aur / f
            if src.is_file():
                if f == "gtk.css":
                    shutil.copyfile(src, root / "config/includes.chroot/etc/skel/.config/gtk-3.0/gtk.css")
                else:
                    shutil.copyfile(src, skel_current / f)
        shutil.copyfile(bgs / "aurora-night.png", skel_current / "wallpaper")
        (skel_current / "theme-name").write_text("Aurora Night")
        # perf variant fallback (opaque) until first theme switch
        css = (aur / "waybar.css").read_text()
        (skel_current / "waybar-perf.css").write_text(css)
        print("out-of-box theme: Aurora Night wired into /etc/skel")
    return 0


if __name__ == "__main__":
    sys.exit(main())
