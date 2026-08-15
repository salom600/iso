#!/usr/bin/env bash
# Install everything needed on a Debian 12/13 host to build Borealis Linux.
# Idempotent — safe to re-run. Works on bare hosts and debian:* containers.
set -euo pipefail

export DEBIAN_FRONTEND=noninteractive

SUDO=""
[[ $EUID -eq 0 ]] || SUDO="sudo"

# The debian:bookworm container image ships sources with `main` ONLY, but
# Borealis needs all four components (firmware -> non-free-firmware,
# steam-installer -> contrib, nvidia -> non-free). Add a full-component
# sources file so package pre-flight and installs resolve.
if grep -q '^ID=debian' /etc/os-release 2>/dev/null; then
    CODENAME=$(. /etc/os-release && echo "${VERSION_CODENAME:-bookworm}")
    $SUDO tee /etc/apt/sources.list.d/borealis-build.sources >/dev/null <<EOF
Types: deb
URIs: http://deb.debian.org/debian
Suites: ${CODENAME} ${CODENAME}-updates
Components: main contrib non-free non-free-firmware
Signed-By: /usr/share/keyrings/debian-archive-keyring.gpg

Types: deb
URIs: http://security.debian.org/debian-security
Suites: ${CODENAME}-security
Components: main contrib non-free non-free-firmware
Signed-By: /usr/share/keyrings/debian-archive-keyring.gpg
EOF
fi

$SUDO apt-get update -qq

# Core build tooling — strict (build cannot proceed without these).
$SUDO apt-get install -y --no-install-recommends \
    live-build debootstrap \
    xorriso mtools syslinux syslinux-common isolinux \
    grub-pc-bin grub-efi-amd64-bin \
    python3 python3-pil ca-certificates curl git sudo

# 32-bit UEFI injection support (optional).
$SUDO apt-get install -y --no-install-recommends grub-efi-ia32-bin || true

echo "Build host ready."
