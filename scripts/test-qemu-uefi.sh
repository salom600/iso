#!/usr/bin/env bash
# Boot a Borealis ISO in QEMU with UEFI firmware (OVMF).
# Usage: scripts/test-qemu-uefi.sh <iso> [ram_MB]
set -euo pipefail
ISO="${1:?usage: test-qemu-uefi.sh <iso> [ram_MB]}"
RAM="${2:-4096}"

OVMF=""
for f in /usr/share/OVMF/OVMF_CODE_4M.fd /usr/share/ovmf/OVMF.fd /usr/share/OVMF/OVMF.fd; do
    [ -f "$f" ] && OVMF="$f" && break
done
[ -n "$OVMF" ] || { echo "OVMF not installed (apt install ovmf)"; exit 1; }

# work on a writable copy: qemu needs to write NVRAM next to the firmware
TMP=$(mktemp -d /tmp/borealis-ovmf.XXXXXX)
cp "$OVMF" "$TMP/OVMF.fd"

KVM=""
[ -w /dev/kvm ] && KVM="-enable-kvm -cpu host"

exec qemu-system-x86_64 \
    -m "$RAM" -smp 2 $KVM \
    -bios "$TMP/OVMF.fd" \
    -cdrom "$ISO" \
    -display gtk,show-cursor=on \
    -usb -device usb-tablet \
    -netdev user,id=n0 -device virtio-net-pci,netdev=n0 \
    -device virtio-vga \
    -serial stdio
