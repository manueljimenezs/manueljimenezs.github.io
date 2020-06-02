---
layout: post
title: "Full-disk encryption on Archlinux with LVM+LUKS+BTRFS"
categories: guides
date: 2020-05-28 19:19:54 +01:00
---

This article will guide you through a basic Archlinux installation with full-disk encryption and the usage of the BTRFS filesystem for managing subvolumes and snapshots.

The steps shown here are all available in the Arch Wiki, but I wanted to make an installation example from scratch until OS startup.

This installation will presume you are booting from an __EFI System__ and that you will be using a SWAP partition. Again, this is a concrete real-world example but feel free to make it match to your likings.

## Planning the disk layout

<!-- more -->

In this case we're going to make two main partitions in a GPT partition table:

* `/dev/sda1`, the ESP (UEFI Boot Partition) that will hold our kernel and the bootloader. Formatted as FAT32 with a size of 512MB with `mkfs.fat -F 32 /dev/sda1`
* `/dev/sda2`, is a partition that will contain an encrypted container which at the same time will contain an LVM physical volume which at the same time will contain logical volumes for both the __root__ and __swap__ filesystems. Yeah, this seems a little bit crazy but it is a very flexible configuration :)

 ![](/assets/img/2020-05-28-disk-encryption/diagram.png)

## Setting up the disk layout and volumes

Supposing you've already created the two partitions mentioned about and formatted `/dev/sda1` as FAT32, the next step is to create the encrpyted container:
```
# cryptsetup luksFormat /dev/sda2
# cryptsetup open /dev/sda2 cryptlvm
```
Consecutively, a physical volume called ```cryptlvm``` is going to be created. We will also add that physical volume to a volume group called ```secure```
```
# pvcreate /dev/mapper/cryptlvm
# vgcreate secure /dev/mapper/cryptlvm
```
Then we're going to focus on creating the __swap__ and __root__ filesystems:

The __swap__ partition will be 4GB and the rest will be used for the BTRFS system partition
```
lvcreate -L 4G secure -n swap
lvcreate -l 100%FREE secure -n root
```

Initialize the __swap__ partition:
```
mkswap /dev/mapper/secure-swap
swapon /dev/mapper/secure-swap
```

Create the __BTRFS__ filesystem and their subsequent subvolumes: '@' for root, '@home' for the home folder and '@snapshots' for making filesystem backups. This makes it to discriminate directories when making backups.

```
mkfs.btrfs /dev/mapper/secure-system
mount /dev/mapper/secure-system /mnt
btrfs subvolume create /mnt/@
btrfs subvolume create /mnt/@home
btrfs subvolume create /mnt/@snapshots 
umount /mnt
```
Now we're going to mount all the volumes and we're going to enable zstd compression.

```
mount -o subvol=@,compression=zstd /dev/mapper/secure-system /mnt
mkdir -p /mnt/{home,boot}
mount -o subvol=@home,compression=zstd /dev/mapper/secure-system /mnt/home
mount /dev/sda1 /mnt/boot
```

## Continue with the usual Arch install

__Follow the normal install of the base system and basic config. in the [Installation guide](https://wiki.archlinux.org/index.php/installation_guide)__

## Finishing the installation

When arriving at the mkinitcpio part some extra steps will be required:

Install ```intel-ucode``` (or the AMD counterpart) and install systemd-boot on the ESP:

```
bootctl –path=/boot install
```

Head over to the ESP (/boot) and create ```arch.conf``` inside the ```entries``` directory with the following content:

```
title Arch Linux
linux /vmlinuz-linux
initrd /intel-ucode.img       # ONLY FOR INTEL CPUs!!
initrd /initramfs-linux.img
options luks.uuid=<LUKS_UUID> root=/dev/mapper/secure-system rootflags=subvol=@ rd.luks.options=discard
```

__Replace `<LUKS_UUID>` with the UUID shown in `blkid` in the filesystem flagged as LUKS.__

Add `default arch` inside the `loader.conf` file.

Edit the HOOKS line in `/etc/mkinitcpio.conf` with the following modules:

```conf
HOOKS=(base systemd autodetect modconf keyboard sd-vconsole block sd-encrypt sd-lvm2 filesystems fsck)
```

Lastly run `mkinitcpio -p linux` and `reboot`. If you're lucky enough you will enter to your newly installed operating system.



