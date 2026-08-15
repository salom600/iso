# Building Borealis Linux

## Requirements

* A Debian 12 (or 13) machine — bare metal, VM, or **WSL2** (with systemd enabled)
* ~15 GB free disk, 4 GB RAM, internet
* `sudo` rights

## One-command build

```bash
sudo scripts/bootstrap-host.sh   # installs live-build, xorriso, grub tools, PIL, QEMU
./build.sh                       # → borealis-1.0-amd64.iso
```

`build.sh` performs, in order:

1. Verifies every optional package against apt metadata (skips unavailable ones,
   generates `config/package-lists/zz-optional-verified.list.chroot`).
2. Pre-flights the **core** package list — aborts *before* the long build if a
   package name is wrong.
3. Syncs `src/apps/*`, `src/lib/*`, `themes/*`, `calamares/*` into the
   `config/includes.chroot` overlay.
4. Generates artwork (wallpapers, branding logo, out-of-box theme wiring) —
   deterministic (seed 42).
5. `lb config` with bookworm + backports + all four archive areas.
6. `lb build` — 20–60 min.
7. Optional: `ADD_EFI32=1 ./build.sh` injects a 32-bit UEFI bootloader
   (experimental).

Useful env vars: `ISO_VERSION=1.1`, `SKIP_OPTIONAL=1`, `KEEP_CACHE=1`.

## Building without a Debian machine

* **GitHub Actions** (recommended): fork the repo, push, run the
  `Build Borealis Linux ISO` workflow. The ISO is uploaded as an artifact.
* **WSL2**: `wsl --install -d Debian`, enable systemd in `/etc/wsl.conf`
  (`[boot]\nsystemd=true`), then the same commands as above. QEMU/KVM testing
  is limited inside WSL2 — test the ISO on a real machine or in VirtualBox.

## Writing the ISO to USB

The ISO is hybrid — use any of:

```bash
dd if=borealis-1.0-amd64.iso of=/dev/sdX bs=4M status=progress oflag=sync
```

or Rufus (DD mode), Ventoy, or balenaEtcher.

## Testing

```bash
scripts/test-qemu-uefi.sh borealis-1.0-amd64.iso
scripts/test-qemu-bios.sh borealis-1.0-amd64.iso
```

Then work through `TESTPLAN.md`.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `Core package 'X' not found` | Typo or missing repo component — check `borealis-base.list.chroot`; on Debian 13 hosts some package names differ, prefer a Debian 12 host |
| Backports kernel hook fails | The ISO falls back to the stable 6.1 kernel intentionally; to retry, remove `cache/` and rebuild |
| `wine32:i386` skipped in hook | 32-bit Wine unavailable at build time — 64-bit Wine still ships; check mirror access |
| Calamares shows Debian branding | `calamares-settings-debian` got pulled in — hook 0300 purges it; verify it ran (`grep calamares-settings borealis-build.log`) |
| EFI machine won't boot the USB | Re-flash with DD mode; ensure the ISO was not truncated (`sha256sum`) |
| Build dies on `lb build` halfway | `lb clean --purge && ./build.sh`; keep `KEEP_CACHE=1` for faster retry |

## Rebuilds after changes

Editing configs/overlays only: `./build.sh` (full rebuild, deterministic).
Faster iteration: `KEEP_CACHE=1` reuses the debootstrap cache (~8 min saved).
