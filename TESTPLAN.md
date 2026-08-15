# Borealis Linux — Test Plan

Run every item against each built ISO before calling it a release.
QEMU helpers: `scripts/test-qemu-uefi.sh <iso>` and `scripts/test-qemu-bios.sh <iso>`
(VirtualBox: attach ISO, enable EFI in System→Motherboard for the UEFI pass).

## 1. Boot

| # | Test | Steps | Pass criteria |
|---|------|-------|---------------|
| 1.1 | BIOS boot | `test-qemu-bios.sh iso` | GRUB/isolinux menu → live session reaches the Borealis desktop |
| 1.2 | UEFI boot | `test-qemu-uefi.sh iso` | Same as 1.1 via OVMF |
| 1.3 | USB write | `dd` ISO to stick; boot real machine (BIOS + UEFI) | Boots; Rufus DD-mode & Ventoy also OK |
| 1.4 | Boot artwork | watch boot | Plymouth splash, quiet, no error spam |
| 1.5 | Recovery session | log out → pick "Borealis (Recovery X11)" | Openbox session starts |

## 2. Live session (Borealis Shell)

| # | Test | Pass criteria |
|---|------|---------------|
| 2.1 | Autologin | Live session logs in as `borealis` without password |
| 2.2 | Dock | Glass dock bottom-center: launcher, task list, clock, tray, network, volume, boost, quick |
| 2.3 | Start menu | Super+Space and Ctrl+Esc open the launcher; search+Enter launches an app |
| 2.4 | Windows management | Super+arrows snap; Alt+Tab switcher; Super+Tab expo; Super+Q closes |
| 2.5 | Wayland/X11 mix | foot (Wayland) + `xeyes`-class X11 app via XWayland both display |
| 2.6 | Screenshots | Print (full) and Super+Shift+S (region) save file + clipboard |
| 2.7 | Idle footprint | `free -m` after 3 min idle: used < 500 MB; `top`: ~0% CPU |
| 2.8 | Audio/Network applets | Volume keys work; network icon opens nm-connection-editor |
| 2.9 | Quick settings | Super+A: toggles reflect state; volume/brightness sliders act |
| 2.10 | Lock/idle | Super+L locks; unlock works |

## 3. Installer (Calamares) — run each on a throwaway disk

| # | Test | Pass criteria |
|---|------|---------------|
| 3.1 | Erase disk | Completes; reboot into installed system; login screen (no autologin) |
| 3.2 | Alongside Windows | NTFS shrink offered; both OSes boot (grub menu shows both) |
| 3.3 | Manual partitioning | Custom /, swap, /boot/efi scheme installs & boots |
| 3.4 | LUKS (erase + encrypt) | Installs; passphrase asked at boot; system usable |
| 3.5 | Post-install cleanliness | `/etc/lightdm/lightdm.conf.d/20-borealis-live-autologin.conf` gone; no `borealis` user; `/etc/borealis-install-marker` present |
| 3.6 | Installed system | Welcome shows once; theme is Aurora Night; updates work |

## 4. Borealis Store

| # | Test | Pass criteria |
|---|------|---------------|
| 4.1 | APT install | e.g. VLC: password prompt once → installs → shows in Installed |
| 4.2 | APT remove | Removes cleanly |
| 4.3 | Flatpak install | VS Code installs from flathub (user) and launches |
| 4.4 | Updates tab | Counts APT/Flatpak updates; "Update everything" applies them |
| 4.5 | AppImage entry | Entry opens homepage/download path without traceback |
| 4.6 | Error path | Cancel the polkit prompt → clear error text, app stays alive |

## 5. Windows layer

| # | Test | Pass criteria |
|---|------|---------------|
| 5.1 | First .exe run | App/Game choice → prefix created with fonts+vcrun; program launches |
| 5.2 | Game prefix | Games prefix gets DXVK; a D3D9/11 title runs (test e.g. Hollow Knight demo) |
| 5.3 | MSI | .msi installer runs via msiexec |
| 5.4 | Store Windows tab | .NET 4.8 verb installs into apps prefix |

## 6. Game Boost

| # | Test | Pass criteria |
|---|------|---------------|
| 6.1 | Toggle | Quick settings → governor=`performance`, animations off, services paused; indicator shows ON |
| 6.2 | Revert | Toggle off → `schedutil` governor, services back, animations return |
| 6.3 | gamerun | `borealis-gamerun -- glxgears` (XWayland) boosts while running, restores on exit |
| 6.4 | Overlay | MangoHud shows FPS/CPU when installed |

## 7. Themes

| # | Test | Pass criteria |
|---|------|---------------|
| 7.1 | Apply Glacier Light | Wallpaper + dock + GTK + icon theme all switch atomically |
| 7.2 | Apply Aurora Night | Back to dark; lock screen uses theme wallpaper |
| 7.3 | Theme store | Point URL at themes/index.json mirror → download & apply works |
| 7.4 | Import | Import a packed `.borealistheme` via file picker |
| 7.5 | Performance Mode | Toggle: dock goes opaque, animations stop; re-login keeps state |

## 8. Hardware sweep (real machines when available)

- 2008–2012 dual-core, 2–4 GB RAM, HDD → boots < 90 s, usable shell (Performance Mode)
- Broadwell/Skylake iGPU → Wayland native, accelerated
- NVIDIA Kepler+ → one-click driver installer + reboot
- AMD GCN/RDNA → works out of box (RADV Vulkan)
- 32-bit UEFI device → with `ADD_EFI32=1` ISO (experimental, see DEVIATIONS.md)

Regression rule: any failing item → fix → rebuild → re-run the failed section **and** section 1.
