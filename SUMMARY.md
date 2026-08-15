# Borealis Linux 1.0 "Glacier" — Delivery Summary

**What it is**: a Debian 12-based distribution for Windows 11 / macOS
switchers — custom Wayland desktop, one-click software store, Windows-app
layer, gaming mode, wide 2008–2026 hardware support. Free and open source
(MIT for custom code).

**What this repository delivers**: the complete, reproducible build system.
`./build.sh` on a Debian 12 host (or the included GitHub Actions workflow)
produces `borealis-1.0-amd64.iso` — a hybrid BIOS+UEFI live/installer image.

## Composition

| Layer | Choice |
|---|---|
| Base | Debian 12 bookworm, main+contrib+non-free+non-free-firmware, systemd tuned (no background apt/man-db timers, journald capped, zram swap) |
| Kernel | 6.12 LTS from backports (stable 6.1 fallback), microcode, full firmware set |
| Desktop | **Borealis Shell**: Wayfire 0.7 floating desktop + custom glass dock (waybar) + launcher + quick settings + notifications; XWayland for X11 apps; openbox recovery session. No XFCE/LXQt anywhere |
| Identity | Aurora Night (anime-inspired dark) + Glacier Light themes; Theme engine changes wallpaper/GTK/dock/icons atomically; Theme Store with community index + `.borealistheme` packs |
| Software | **Borealis Store** (GTK3): search/install/update across APT, Flatpak (flathub), Snap, AppImage; updates tab; curated catalog |
| Windows apps | Wine 64+32 (i386 multiarch), winetricks-managed prefixes (apps/games), auto DXVK for games, `.exe` double-click integration, Store "Windows" tab |
| Gaming | Feral GameMode, MangoHud, Steam, Lutris*, **Game Boost** (governor→performance, services paused, effects off, one-click or `borealis-gamerun`) |
| Installer | Calamares: erase / alongside Windows / manual / LUKS, Borealis branding, live-artifact cleanup on install |
| Hardware | BIOS+UEFI x64 boot, hybrid ISO (dd/Rufus/Ventoy/Etcher), open GPU drivers + one-click NVIDIA installer, 32-bit UEFI injector (experimental) |

## Performance targets (design, verify with TESTPLAN §2.7)

* Idle RAM: ~250–350 MB in the live shell (target < 500 MB)
* Idle CPU: ~0 % — no indexing/telemetry/auto-update daemons
* Performance Mode: opaque dock, zero animations — for 2008–2015 GPUs

## Included custom software (all MIT)

`borealis-session · -bar · -menu · -quick · -settings · -store · -welcome ·
-screenshot · -lock · -wallpaper · -wm-helper · -cpugov · -gameboost-sys ·
-boost · -boost-indicator · -perf · -gamerun · -wine · -exe-launcher ·
-appimage-launcher · -driver-installer · -updater` + shared theme library +
2 themes + catalogs + Calamares branding.

## Instructions

* Build: **BUILDING.md** (Debian host / WSL2 / GitHub Actions)
* Use: **USAGE.md** (end-user manual)
* Verify: **TESTPLAN.md** (BIOS/UEFI, installer modes, store, wine, boost, themes)
* Known limits: **DEVIATIONS.md** (12 documented items, most notable: no
  prebuilt ISO binary from this Windows-based session; Wayfire 0.7 blur/SSD
  limits; auto-fullscreen boost deferred)
