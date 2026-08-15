#!/bin/sh
# pack-theme.sh — package a theme directory for the Borealis Theme Store.
#
#   themes/pack-theme.sh themes/my-theme
#     -> my-theme-<version>.borealistheme (tar.gz with a top-level <slug>/ dir)
#
# Theme directory layout:
#   theme.json   (slug, name, version, author, description, variant,
#                 accent, preview_bg, wallpaper, icons, cursor, font)
#   gtk.css      GTK3 overlay
#   waybar.css   dock style
#   wallpaper.png
set -eu

dir="${1:?usage: pack-theme.sh <theme-dir>}"
dir="${dir%/}"
slug=$(basename "$dir")
[ -f "$dir/theme.json" ] || { echo "no theme.json in $dir" >&2; exit 1; }

version=$(python3 -c "import json;print(json.load(open('$dir/theme.json')).get('version','1.0'))")
for f in gtk.css waybar.css "$(python3 -c "import json;print(json.load(open('$dir/theme.json')).get('wallpaper','wallpaper.png'))")"; do
    [ -f "$dir/$f" ] || { echo "missing file: $dir/$f" >&2; exit 1; }
done

out="${slug}-${version}.borealistheme"
tar -C "$(dirname "$dir")" -czf "$out" "$slug"
echo "packed: $out"
echo "publish: upload to the themes repository and add an entry to index.json"
