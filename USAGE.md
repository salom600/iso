# Using Borealis Linux

A short manual for the incoming Windows 11 / macOS user.

## The desktop in 60 seconds

* **Dock** (bottom, glass): Start ◆ · running apps · clock · tray · network ·
  volume · Game Boost · quick settings ⚙
* **Start menu**: `Super+Space` (or `Ctrl+Esc` — the Windows 11 habit works)
* **Snap a window**: `Super+Arrow keys` (just like Windows)
* **Switch apps**: `Alt+Tab` · **Desktops**: `Super+Tab`
* **Quick settings**: `Super+A` — Wi-Fi, Bluetooth, volume, brightness,
  Performance Mode, Game Boost, Night Light, Do Not Disturb
* **Settings**: `Super+I` · **Terminal**: `Super+T` · **Files**: `Super+E`
* **Screenshot**: `Print` (full) · `Super+Shift+S` (snip)
* **Lock**: `Super+L`

Full table in Borealis Settings → Shortcuts.

## Install the system

Live session → **Install Borealis Linux** on the desktop/dock:

* **Erase disk** — simplest, whole disk
* **Replace a partition / Install alongside** — shrink Windows and share the
  disk (GRUB will offer both OSes at boot)
* **Manual partitioning** — full control
* **Encrypt** (erase mode) — LUKS full-disk encryption, passphrase at boot

You pick language, timezone, keyboard, username and password. That's it.

## Software: Borealis Store

One search box across **APT** (Debian repo), **Flatpak** (Flathub), **Snap**
and **AppImage**, plus a **Windows** tab. Updates are manual by design —
`Store → Updates → Update everything`, or Welcome → "Check for updates".

## Windows programs

Double-click any `.exe`. The first run prepares a Wine prefix (internet
needed once): fonts, Visual C++ runtimes — games additionally get **DXVK**
(DirectX→Vulkan). Prefer native alternatives from the Store when available.

## Gaming

* Toggle **Game Boost** (dock or `Super+A`): CPU governor to performance,
  background services pause, animations off — restore with one click.
* Per-game acceleration: `borealis-gamerun -- %command%` in Steam launch
  options, or prefix any binary (`borealis-gamerun -- ./game`).
  Adds GameMode (process priority) + MangoHud overlay automatically.
* Steam (APT) and Lutris (Store) integrate with the same stack; Proton-GE via
  ProtonUp-Qt (Store → Flatpak).

## Performance Mode

`Super+A → Performance` (or Settings → Performance): disables animations and
transparency for old GPUs and RDP sessions. Persists across reboots.

## Themes & wallpapers

Settings → Appearance. Themes change wallpaper + dock + GTK apps + icons in
one click. **Theme Store** (Settings) downloads community themes; anyone can
pack one: `themes/pack-theme.sh my-theme` → submit a PR to the themes repo.

## Drivers

AMD and Intel work out of the box (open drivers + Vulkan). NVIDIA: Welcome →
"Install drivers", or Borealis Store → System. Reboot when prompted.

## Where things live

| What | Where |
|---|---|
| Your apps (AppImages) | `~/Applications` |
| Wine prefixes | `~/Wine/apps`, `~/Wine/games` |
| Screenshots | `~/Pictures/Screenshots` |
| Themes (user-installed) | `~/.local/share/borealis/themes` |
| Current theme assets | `~/.local/share/borealis/current` |

## Recovery

Login screen → session picker → **Borealis (Recovery X11)** is a minimal
openbox session for fixing driver issues; reinstall drivers from a terminal
(`pkexec apt-get install --reinstall ...`) or chroot in from the live USB.
