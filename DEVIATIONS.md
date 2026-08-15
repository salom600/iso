# Deviations from the Original Specification

Engineering honesty log. Each entry states what was specified, what shipped,
and why.

## 1. No finished ISO binary in this delivery
**Spec**: "Provide the final ISO file."
**Shipped**: complete, reproducible build system producing the ISO with one
command on Debian/WSL2, plus a CI workflow that builds and uploads it.
**Why**: the build environment available for this task is a Windows host;
`live-build`/`debootstrap` require a Debian host. Every ingredient needed for
the ISO — package lists, hooks, overlays, installer config, artwork
generation — is in the repository and deterministic (seeded artwork, pinned
package lists). Section order in `build.sh` mirrors the required pipeline.

## 2. Kernel: 6.12 LTS instead of "6.6 LTS or newer"
Spec allowed ≥ 6.6; `bookworm-backports` currently carries the **6.12 LTS**
line, which is what the build installs (hook 0100). If backports is
unreachable at build time the image intentionally falls back to Debian 12's
6.1 LTS (still broad hardware coverage) and the build log warns.

## 3. Desktop: Wayfire 0.7 (Debian 12) — blur/rounded-window corners limited
**Spec**: glassmorphism/acrylic, rounded corners, animations.
**Shipped**: animations, transparency-based glass dock/menus/notifications,
rounded panels — all real. **True compositor-side blur and rounded window
corners require Wayfire ≥ 0.8 / wlroots 0.17**, which are not in bookworm
(building them from source would chain two source builds and hurt
reproducibility). Visual glass effect is achieved with alpha transparency,
which composites cheaply — arguably better for the 2008-hardware goal.
Performance Mode swaps all translucency for opaque styles automatically.

## 4. X11 apps under Wayfire 0.7 have no server-side decorations
CSD apps (GTK/Qt/Electron) decorate themselves; XWayland apps (incl. Wine)
open without SSD title bars. Mitigation shipped: Wine game/app windows run
in Wine's virtual-desktop mode for sane geometry; the recovery X11 session
is openbox. Wayfire 0.8 (Debian 13 base) resolves this fully — noted as the
v2 upgrade path.

## 5. "Optional-verified" package tier
Packages whose presence in bookworm could not be pinned with 100 % certainty
(`wofi`, `bemenu`, `mangohud`, `lutris`, `gamescope`, `thermald`, `wlsunset`,
`fonts-inter`, `breeze-cursor-theme`, `fonts-jetbrains-mono`, `btop`,
`powertop`, `inxi`, `fwupd`, `qt6-wayland`) are verified against apt at build
time and installed only if resolvable. UX degrades explicitly and gracefully:
launcher falls back wofi→bemenu→zenity; Game Boost works without MangoHud;
the dock works without custom cursors. This keeps `lb build` from aborting
40 minutes in over a single name.

## 6. Auto-fullscreen Game Boost detection
**Spec**: automatic resource redirection when a fullscreen app is detected.
**Shipped**: explicit toggles (Quick Settings / dock) + per-process wrapper
`borealis-gamerun` with automatic restore-on-exit. Reason: Wayfire 0.7
exposes no IPC/foreign-toplevel CLI to watch focus/fullscreen state without
shipping a bespoke protocol client; heuristic CPU-spiking detection produces
false positives (compiles, video encodes) that would degrade the wrong apps.
Roadmap: wf-shell/foreign-toplevel watcher when the base moves to Wayfire
0.8.

## 7. 32-bit UEFI: helper script, not default
A 64-bit-only ISO with an experimental post-build injector
(`scripts/add-efi32.sh`, `ADD_EFI32=1`). Repacking the El Torito image is
firmware-sensitive; it ships as opt-in rather than risking every user's boot.

## 8. Snap support present but low-priority
snapd ships socket-activated (zero idle cost). The Store can use it, but the
default catalog surfaces APT/Flatpak first — better integration with the
system and no snap-specific quirks on a Wayland-only desktop.

## 9. Broadcom BCM43xx (2008–2012 Macs) legacy `wl` driver not preinstalled
`broadcom-sta-dkms` requires kernel headers + out-of-tree module (size, DKMS
fragility, GPL-compatibility debates). `firmware-brcm80211` covers the
newer chipsets; for `wl`-only chips USAGE/BUILDING point to a one-liner
(`sudo apt install broadcom-sta-dkms linux-headers-$(uname -r)`).

## 10. No telemetry-gated niceties
Indexing services, update automation, popularity-contest — deliberately
absent to honor "idle CPU ~0 %". Updates are user-initiated by design.

## 11. Branding placeholder
"Borealis Linux" is a working identity; URLs point at `*.example`
placeholders. Before public distribution: register the domain, rename
branding URLs, and do a trademark sweep — no affiliation with Debian,
Microsoft, Apple or Valve is implied.

## 12. VM test execution
The test harness (QEMU UEFI/BIOS scripts + TESTPLAN.md matrix) is complete
but could not be executed on the Windows host available for this task.
The CI workflow can be extended (`workflow_dispatch` input → run scripts)
to smoke-test boot in GitHub's runners.
