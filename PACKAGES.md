# Borealis Linux — Package Manifest

Everything below installs into the image. ~2.2–2.6 GB ISO.
Kernel: **6.12 LTS (bookworm-backports)** via hook, stable 6.1 as build fallback.

## Base & platform
debian-12 minimal (live-build/debootstrap) · systemd (tuned) · live-boot ·
live-config · `linux-image-amd64` · `intel-microcode` `amd64-microcode` ·
`memtest86+` · `zram-tools` · `irqbalance` · `lm-sensors` · `upower` ·
`udisks2`

## Firmware (non-free-firmware + free)
`firmware-linux(-nonfree)` · `firmware-misc-nonfree` · `firmware-amd-graphics` ·
`firmware-iwlwifi` · `firmware-atheros` · `firmware-brcm80211` ·
`firmware-realtek` · `firmware-mediatek` · `firmware-sof-signed` ·
`bluez-firmware`

## Borealis Shell (desktop)
`wayfire` (Wayland compositor, floating desktop) · `waybar` (glass dock) ·
`wofi`/`bemenu`* (launcher; zenity fallback built in) · `foot` (terminal) ·
`mako-notifications` · `swaybg` `swaylock` `swayidle` · `grim` `slurp` (screenshots) ·
`wl-clipboard` · `xwayland` (X11 apps) · `qtwayland5` ·
`lightdm` + `lightdm-gtk-greeter` · `policykit-1-gnome` ·
`xdg-desktop-portal{-wlr,-gtk}` · `openbox`+`xterm` (recovery session) ·
`plymouth`

## Applications
`firefox-esr` · `nemo` (+gvfs backends) · `gnome-text-editor` · `mpv` ·
`file-roller` `p7zip-full` `unzip` · `zenity` · `gparted` ·
`gnome-disk-utility` · `htop`/`btop`* · `cups` + `system-config-printer`
(printers) · `blueman` (Bluetooth) · `nm-applet` (network)

## Multimedia stack
`pipewire` `pipewire-pulse` `pipewire-alsa` `wireplumber`
`libspa-0.2-bluetooth` · `pavucontrol`

## Graphics / compute
`mesa-vulkan-drivers` (RADV/ANV) · `libvulkan1` `vulkan-tools` · `mesa-utils`
· NVIDIA proprietary: **not preinstalled** — one-click via
`borealis-driver-installer` (kept out for size + licensing; nouveau works
everywhere at basic level)

## Gaming
`gamemode` (Feral) · `steam-installer` (contrib) · `mangohud`* · `lutris`* ·
`gamescope`* — plus custom `borealis-boost` / `borealis-gamerun` stack

## Windows layer
`wine` + `wine64` + `wine32:i386` (multiarch, hook 0200) · `winetricks` ·
`winbind` `cabextract` · 32-bit Vulkan libs for DXVK

## Store & apps runtime
`python3-gi` `gir1.2-gtk-3.0` `python3-apt` `python3-requests` · `flatpak`
(flathub user remote, preconfigured by the Store) · `snapd` (socket-activated;
zero resident cost until used)

## Installer
`calamares` · `grub-pc` + `grub-efi-amd64` (+ `-bin`) · `efibootmgr` ·
`os-prober` (Windows detection in dual boot) · `cryptsetup` `lvm2` (LUKS
installs) · `ntfs-3g` `dosfstools` `exfatprogs`

## Fonts & icons
`fonts-noto-core` `fonts-noto-color-emoji` `fonts-liberation` `fonts-cantarell`
· `fonts-jetbrains-mono`* · `papirus-icon-theme` + `adwaita-icon-theme`

## Custom Borealis components (overlay, MIT)
`borealis-session` `borealis-bar` `borealis-menu` `borealis-quick`
`borealis-settings` `borealis-store` `borealis-welcome` `borealis-screenshot`
`borealis-lock` `borealis-wallpaper` `borealis-wm-helper` · Game Boost:
`borealis-cpugov` `borealis-gameboost-sys` `borealis-boost`
`borealis-boost-indicator` `borealis-perf` `borealis-gamerun` · Windows layer:
`borealis-wine` `borealis-exe-launcher` `borealis-appimage-launcher` ·
Maintenance: `borealis-driver-installer` `borealis-updater` · Themes:
Aurora Night, Glacier Light · Catalogs (AppImage / Windows / theme store)

\* = "optional-verified": installed when the package resolves on the build
host, features degrade gracefully otherwise (see DEVIATIONS.md §5).
