#!/usr/bin/env python3
"""verify-hybrid.py — structural check that an ISO is a bootable hybrid image:
  * ISO9660 with an El Torito boot catalog
  * a BIOS (legacy, no-emulation) boot entry
  * a UEFI (platform 0xEF section) boot entry
  * MBR signature 0x55AA with a GPT-protective or whole-image partition
    => burnable to DVD (El Torito BIOS+UEFI) and raw-dd-able to USB flash
Usage: verify-hybrid.py <iso>
"""
import struct
import sys


def main(path):
    f = open(path, "rb")

    f.seek(16 * 2048)
    pvd = f.read(2048)
    ok_iso = pvd[1:6] == b"CD001"
    print(f"ISO9660 PVD: {'OK' if ok_iso else 'MISSING'}")

    f.seek(17 * 2048)
    brvd = f.read(2048)
    ok_br = brvd[1:6] == b"CD001" and brvd[0:1] == b"\x00"
    cat_sec = struct.unpack("<I", brvd[71:75])[0] if ok_br else None
    print(f"El Torito boot record: {'OK (catalog @ sector %d)' % cat_sec if ok_br else 'MISSING'}")

    bios_ok = efi_ok = False
    if cat_sec is not None:
        f.seek(cat_sec * 2048)
        cat = f.read(2048)
        platform = 0x00  # platform of the current section
        i = 0
        while i < len(cat):
            kind = cat[i]
            if kind == 0x01:                      # validation entry
                platform = cat[i + 4]
            elif kind in (0x90, 0x91):            # section header
                platform = cat[i + 1]
            elif kind in (0x88, 0x00):            # boot / section entry
                media = cat[i + 1]
                if kind == 0x88 and media == 0:
                    if platform in (0x00,):
                        bios_ok = True
                    if platform == 0xEF:
                        efi_ok = True
            elif kind == 0x55:                    # final section header
                break
            i += 32
    print(f"El Torito BIOS boot entry: {'OK' if bios_ok else 'MISSING'}")
    print(f"El Torito UEFI boot entry (platform 0xEF): {'OK' if efi_ok else 'MISSING'}")

    f.seek(0, 2)
    total = f.tell()
    f.seek(510)
    mbr_ok = f.read(2) == b"\x55\xaa"
    print(f"MBR signature 0x55AA: {'OK' if mbr_ok else 'MISSING'}")

    span_ok = False
    detail = ""
    if mbr_ok:
        f.seek(446)
        for n in range(4):
            pe = f.read(16)
            boot, ptype = pe[0], pe[4]
            lba = struct.unpack("<I", pe[8:12])[0]
            nsec = struct.unpack("<I", pe[12:16])[0]
            end = (lba + nsec) * 512
            if ptype == 0xEE and nsec * 512 >= total - 1024 * 1024:
                span_ok, detail = True, f"GPT-protective entry spanning {nsec*512/1e9:.2f} GB"
                break
            if boot == 0x80 and nsec and end >= total - 2048 * 512:
                span_ok, detail = True, f"bootable entry type {ptype:#04x} covering {lba*512/1e6:.0f} MB..{end/1e9:.2f} GB"
                break
    print(f"Whole-image boot partition (dd-to-USB): {'OK — ' + detail if span_ok else 'CHECK'}")

    verdict = ok_iso and ok_br and bios_ok and efi_ok and mbr_ok and span_ok
    print("\nVERDICT:", "HYBRID OK — boots from DVD (BIOS+UEFI) and raw-dd USB flash"
          if verdict else "NOT fully hybrid — see lines above")
    return 0 if verdict else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
