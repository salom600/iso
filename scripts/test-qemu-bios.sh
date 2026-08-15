#!/usr/bin/env bash
# Boot a Borealis ISO in QEMU with legacy BIOS (SeaBIOS).
# Usage: scripts/test-qemu-bios.sh <iso> [ram_MB]
set -euo pipefail
ISO="${1:?usage: test-qemu-bios.sh <iso> [ram_MB]}"
RAM="${2:-4096}"

KVM=""
[ -w /dev/kvm ] && KVM="-enable-kvm -cpu host"

exec qemu-system-x86_64 \
    -m "$RAM" -smp 2 $KVM \
    -cdrom "$ISO" \
    -display gtk,show-cursor=on \
    -usb -device usb-tablet \
    -netdev user,id=n0 -device virtio-net-pci,netdev=n0 \
    -device virtio-vga \
    -serial stdio
