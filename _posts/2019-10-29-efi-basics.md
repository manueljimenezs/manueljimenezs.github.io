---
layout: post
title: "EFI Basics: Booting your systems like a pro"
categories: guides
---

![Refind Bootloader](/assets/img/refind_scr.png)

# Introduction
From the year 2013, Microsoft switched its operating system's booting mode to a technology called EFI, already being used in Macs for a long time.

In UEFI (The PC implementation) multiple applications can coexist, this means you can combine multiple bootloaders such as Windows Boot, GRUB, systemd-boot without taking over each other.

# EFI Requirements
 * Your motherboard has to be supported (>2013)
 * Your disk has to be formatted in GPT instead of MBR
 * You need an ESP (EFI system partition) that stores all the *bootable* executables

 ## The ESP

The ESP (EFI system partition) is a small FAT32 partition (~512MB) that stores all the bootloaders:

```
.
├── Boot
│   ├── BOOT.CSV
│   ├── bootx64.efi
│   └── ref.bak
├── Microsoft
│   ├── Boot
│   └── Recovery
├── refind
│   ├── BOOT.CSV
│   ├── drivers_x64
│   ├── icons
│   ├── keys
│   ├── refind.conf
│   ├── refind.conf.bak
│   ├── refind_x64.efi
│   └── themes
├── tools
└── ubuntu
    ├── fw
    └── fwupx64.efi
```

The default bootloader is stored in the firmware level in something we call *EFI Variables* that we'll configure in just a moment. In some motherboards the default bootloader can be chosen in the motherboard config screen.

The `Boot` directory is a fallback option just in case those variables are not set, you could copy any `.efi` file in other folder to `bootx64.efi` to make it your fallback option.

# rEFInd

rEFInd is a graphic bootloader that is smart enough to find the bootable entries without much configuration, it is also able to remember the last booted option to be selected on the next boot. It is also able to boot USB sticks and be bootable from any install media.

## Manual install

Supposing you have an ESP partition in a GPT disk (If you are using Windows 10, you probably are) you just have to copy [the refind folder](https://sourceforge.net/projects/refind/files/0.11.4/refind-bin-0.11.4.zip/download) into the /EFI folder of the ESP (There are also OS-specific installers that do this)

Once copied you have to tell your motherboard to boot from it by default.

In Linux there is an utility that list the boot order called `efibootmgr`

```
BootCurrent: 0002
Timeout: 1 seconds
BootOrder: 0002,0000,0006,0001,0003,0004
Boot0000* Windows Boot Manager
Boot0001* UEFI:CD/DVD Drive
Boot0002* rEFInd Boot Manager
Boot0003* UEFI:Removable Device
Boot0004* UEFI:Network Device
Boot0006* proxmox
```

To add rEFInd:

`efibootmgr -c -l \\EFI\\refind\\refind_x64.efi -L rEFInd`

To change the boot order:

`efibootmgr -o 0,1,2`

To remove an entry:

`efibootmgr -Bb 0000`

Refind has a `refind.conf` and lots of themes to customize it.

## Adding Linux

Windows is automatically detected by refind and some Linux distros too, but if you want to be sure add a `refind_linux.conf` file into your Linux Partition in the `/boot/` directory:

```
"Boot using default options"     "root=PARTUUID=a9fbd673-2ba9-4dcd-be6b-97423dd74c89 rw initrd=/boot/amd-ucode.img initrd=/boot/initramfs-%v.img"
```

the root points to the ID of the partition in which the distro is installed, it can be retrieved with `blkid`.







