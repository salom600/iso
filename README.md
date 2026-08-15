# Borealis Linux 1.0 "Glacier"

**A fast, modern, glassy Linux distribution for people switching from Windows 11 and macOS.**
Built on Debian 12 (Bookworm). Light enough for a 2008 laptop, polished enough for a 2026 desktop.

![license](https://img.shields.io/badge/code-MIT-blue) ![base](https://img.shields.io/badge/base-Debian%2012-red) ![shell](https://img.shields.io/badge/shell-Borealis%20Shell%20(Wayland)-62d0ff)

---

## What is Borealis Linux?

Borealis Linux is a complete custom distribution assembled from Debian 12 packages with a
fully original desktop experience:

| Area | Choice | Why |
|---|---|---|
| Base | Debian 12 minimal (`live-build` + `debootstrap`) | Rock-solid package base, huge hardware/software catalog |
| Kernel | **6.12 LTS** from `bookworm-backports` | Modern hardware (2016–2026) while keeping broad legacy support |
| Init | systemd (tuned: timers trimmed, journald capped, zram) | Compatibility + predictable boot |
| Desktop | **Borealis Shell** — Wayfire (Wayland) + custom dock/launcher/settings | Idle RAM ≈ 250–350 MB, unique identity, XWayland for X11 apps |
| Installer | Calamares (graphical): erase / alongside / manual / **LUKS** | Windows-user friendly |
| Software | **Borealis Store** — one app for APT + Flatpak + Snap + AppImage | One-click install/remove/update with dependency handling |
| Windows apps | Wine (64+32-bit multiarch) + winetricks-managed prefixes + DXVK | Double-click a `.exe` and it runs |
| Gaming | GameMode, MangoHud, VKD3D/Vulkan stack, **Game Boost** mode | One-toggle performance mode + per-game wrapper |
| Hardware | linux-firmware set, intel/amd microcode, BIOS + UEFI (+ 32-bit UEFI helper), open GPU drivers + one-click NVIDIA installer | 2008 → 2026 coverage |

**Not used anywhere:** XFCE, LXQt (explicit project constraint).

## Highlights

- **Borealis Shell** — floating window desktop with a centered glass dock (Windows 11 × macOS
  hybrid), app menu on `Super+Space`, Alt-Tab switcher, virtual desktops, expo, subtle
  animations, screenshot and lock tooling, notifications.
- **Performance Mode** — one toggle: kills animations/transparency, opaque dock, minimal
  shadow work. Made for 2008-era GPUs.
- **Game Boost** — one toggle (or per-game `borealis-gamerun` wrapper): CPU governor →
  `performance`, background services paused, shell effects off, MangoHud overlay, GameMode
  renice. Auto-reverts on exit.
- **Theme Engine + Theme Store** — themes change wallpaper, GTK style, dock style, icons and
  accents atomically. Ships with *Aurora Night* (dark, anime-inspired starry sky) and
  *Glacier Light* (clean professional). Community themes via a simple JSON index.
- **Borealis Store** — unified catalog across APT/Flatpak/Snap/AppImage, categories,
  updates tab, clear error reporting.
- **Windows Layer** — `.exe` double-click launches through a managed Wine prefix; games get a
  DXVK-enabled prefix automatically; store offers curated Windows installers.

## Quick facts

```
Idle RAM (live, Borealis Shell):  ~250–350 MB   (target <500 MB ✓)
Idle CPU:                         ~0%           (no indexing/telemetry services)
ISO size:                         ~2.2–2.6 GB   (hybrid: BIOS + UEFI + dd/Rufus/Ventoy)
Architectures:                    x86_64 (+ i386 multiarch for Wine32/Steam)
Boot:                             BIOS/Legacy/CSM, UEFI x64, 32-bit UEFI (helper script)
```

## Repository layout

```
borealis-linux/
├── build.sh                    # one-command ISO build (Debian 12 host / WSL2 / CI)
├── config/                     # live-build configuration tree
│   ├── package-lists/          # what gets installed into the image
│   ├── hooks/live/             # backports kernel, i386+Wine, systemd tuning
│   └── includes.chroot/        # overlay: /etc/skel, /usr/bin, /usr/share/borealis …
├── calamares/                  # installer settings + Borealis branding
├── src/                        # custom applications (Python/GTK3)
│   ├── borealis-store/         # software center
│   ├── borealis-settings/      # settings + theme manager + theme store
│   ├── borealis-quick/         # quick-settings popover
│   └── borealis-welcome/       # first-run wizard
├── themes/                     # default themes + theme packaging tool
├── scripts/                    # host bootstrap, package verification, artwork gen,
│                               # QEMU test harness, EFI32 helper
├── .github/workflows/          # CI: build the ISO on a GitHub runner
├── BUILDING.md                 # how to build & test
├── USAGE.md                    # end-user guide
├── PACKAGES.md                 # shipped package manifest + rationale
├── TESTPLAN.md                 # verification matrix (BIOS/UEFI, installer, wine, boost)
└── DEVIATIONS.md               # honest engineering deviations from the spec
```

## Build the ISO

On any Debian 12 (or 13) machine, WSL2, or CI:

```bash
git clone <this-repo> borealis-linux && cd borealis-linux
sudo scripts/bootstrap-host.sh     # installs live-build and friends (idempotent)
./build.sh                        # produces borealis-1.0-amd64.iso
```

Or fork and push — `.github/workflows/build-iso.yml` builds the ISO on GitHub's runners and
uploads it as an artifact.

Write to USB with `dd`, Rufus (DD mode), Ventoy, or balenaEtcher — the ISO is hybrid.

## License

Custom code (src/, scripts/, config overlays, themes): **MIT** (see `LICENSE`).
Everything installed from Debian repositories keeps its original license.
"Borealis Linux" is a project codename — see DEVIATIONS.md § branding.
