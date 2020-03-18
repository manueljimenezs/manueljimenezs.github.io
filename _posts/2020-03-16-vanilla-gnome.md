---
layout: post
title: "Running vanilla GNOME on Ubuntu"
categories: tips
date: 2020-03-16 20:19:54 +01:00
---

* Install `gnome-session` and some components:
`sudo apt install gnome-session gnome-tweaks chrome-gnome-shell`

* Restore the default login screen style:
`sudo update-alternatives --config gdm3.css`

 Select `/usr/share/gnome-shell/theme/gnome-shell.css`

 **Log out** from your PC and switch the session to GNOME by clicking the gear icon

Go to extensions.gnome.org and install the User Themes extension

Go to Tweaks and set themes, icons, etc in Adwaita 

 ![](/assets/img/2020-03-16-vanilla-gnome/tweaks-style.png)

# Removing snapd

Snaps are a self-contained package technology that allows software to be installed without worrying about incompatible libraries. The downside is that apps are bigger in size and the startup may be slower.

```sh
sudo rm -rf /var/cache/snapd/

sudo apt autoremove --purge snapd gnome-software-plugin-snap

rm -rf ~/snap
```

You may have to run `apt install gnome-calculator gnome-system-monitor` to get back some default applications that were initially shipped as snaps.
