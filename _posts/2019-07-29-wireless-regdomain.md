---
layout: post
title: "Optimizing the Wi-Fi speed on Linux"
categories: tips
---

Recently I discovered that by default, the Linux kernel may restrict the capabilities of your wireless card because it is set into a _generic world regulatory domain_. This can lead to slower wireless speeds.

The [ArchWiki](https://wiki.archlinux.org/index.php/Wireless_network_configuration#Respecting_the_regulatory_domain) shows how to change the regulatory domain to match your country and optimize your speeds.

First you have to install the package `crda`

Then you have to edit the `/etc/conf.d/wireless-regdom` file and uncomment the respective country.

Running `iw reg get` shows what regulatory country are you in:

```conf
global
country ES: DFS-ETSI
	(2400 - 2483 @ 40), (N/A, 20), (N/A)
	(5150 - 5250 @ 80), (N/A, 23), (N/A), NO-OUTDOOR, AUTO-BW
	(5250 - 5350 @ 80), (N/A, 20), (0 ms), NO-OUTDOOR, DFS, AUTO-BW
	(5470 - 5725 @ 160), (N/A, 26), (0 ms), DFS
	(5725 - 5875 @ 80), (N/A, 13), (N/A)
	(57000 - 66000 @ 2160), (N/A, 40), (N/A)
```

In my case the speed for transferring a local file increased from 6 MB/s to 10 MB/s

