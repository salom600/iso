#!/usr/bin/env bash
#
# add-efi32.sh — experimental: inject a 32-bit GRUB EFI bootloader into a
# finished Borealis ISO so some 32-bit-UEFI devices (2008–2015 Bay Trail /
# Clover Trail tablets and old Macs) can boot the 64-bit system.
#
# Usage: add-efi32.sh <in.iso> <out.iso>
#
# How: extract the ISO's efi.img (FAT), add /EFI/BOOT/BOOTIA32.EFI built with
# grub-mkimage, then rebuild the ISO keeping the original boot catalog.
# If any step fails, keep the original ISO untouched.

set -euo pipefail
IN_ISO="${1:?usage: add-efi32.sh in.iso out.iso}"
OUT_ISO="${2:?usage: add-efi32.sh in.iso out.iso}"

TMP="$(mktemp -d /tmp/borealis-efi32.XXXXXX)"
trap 'rm -rf "$TMP"' EXIT

echo "[efi32] extracting efi.img from $IN_ISO"
xorriso -osirrox on -indev "$IN_ISO" -extract /efi.img "$TMP/efi.img" >/dev/null

echo "[efi32] building i386 EFI grub image"
GRUBLIB="/usr/lib/grub/i386-efi"
[[ -d "$GRUBLIB" ]] || { echo "[efi32] grub-efi-ia32-bin not installed"; exit 1; }
grub-mkimage -O i386-efi -o "$TMP/BOOTIA32.EFI" -p /boot/grub \
    fat iso9660 part_gpt part_msdos normal menu linux linuxefi multiboot2 \
    all_video gfxterm gfxterm_background echo test configfile search \
    search_fs_file search_fs_uuid search_label lsmmap reboot halt \
    loadenv gzio xzio efi_gop efi_uga

echo "[efi32] injecting into efi.img"
mmd   -i "$TMP/efi.img"       ::/EFI
mmd   -i "$TMP/efi.img"       ::/EFI/BOOT
mcopy -i "$TMP/efi.img" "$TMP/BOOTIA32.EFI" ::/EFI/BOOT/

echo "[efi32] rebuilding ISO"
# Repack efi.img back into the ISO, preserving El Torito + MBR hybrid boot.
xorriso -indev "$IN_ISO" -outdev "$OUT_ISO" \
        -boot_image keep \
        -update "$TMP/efi.img" /efi.img \
        -map "$TMP/BOOTIA32.EFI" /EFI/BOOT/BOOTIA32.EFI

echo "[efi32] wrote $OUT_ISO"
echo "        (xorriso keeps the original boot catalog; verify on real 32-bit"
echo "         UEFI hardware or with: qemu-system-i386 -bios /usr/share/ovmf/OVMF32.fd)"
