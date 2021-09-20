---
layout: post
title: How I ended up compiling my own Linux kernel
date: 2021-09-20
categories:
---

I didn't expect this day would arrive. It's all fun and games until you buy a cheap graphic card with only a DVI port in it. It works great for FullHD resolutions. The problem is when you have resolutions and framerates bigger than that.

In the Linux kernel, the maximum pixel clock (the speed at which pixels are transmitted over a port) is limited to 165 MHz leading to messing with the images when displaying bigger resolutions than fullHD.

There are two solutions to this problem:
    
  - Using lower resolutions/framertes, this means not taking advantage of e.g ultrawide monitors. (Spoiler: nobody wants this 😛)

  - Tweaking your kernel, increasing the clock ratio and happily use your shiny screen as it was intended.

## Getting your hands dirty

After a long journey searching on the interwebs, I found that increasing the pixel clock to 250 MHz is enough for WFHD resolutions. There is even a [calculator](https://www.monitortests.com/pixelclock.php) for that.

**Note that you may be running your graphics card out of spec, and you can irreversibly damage your hardware so be very cautious with this.**

Here is the line in the Linux kernel that we're going to change. This change is provide as a patch file, which concisely represents how and where a change in a file is made. Something like `diff --git oldfile.txt newfile.txt` will suffice.

```diff
--- a/drivers/gpu/drm/amd/display/include/signal_types.h	2020-12-17 20:11:00.261706513 +0100
+++ b/drivers/gpu/drm/amd/display/include/signal_types.h	2020-12-17 20:09:14.391997315 +0100
@@ -29,7 +29,7 @@
 /* Minimum pixel clock, in KHz. For TMDS signal is 25.00 MHz */
 #define TMDS_MIN_PIXEL_CLOCK 25000
 /* Maximum pixel clock, in KHz. For TMDS signal is 165.00 MHz */
-#define TMDS_MAX_PIXEL_CLOCK 165000
+#define TMDS_MAX_PIXEL_CLOCK 250000

```

I also created a script that downloads the linux source code, automatically applies all the patches and compiles it with a basic config. [Here](https://github.com/manueljimenezs/linux-build-script) is the full set of files.

```bash
#!/bin/bash
KERNELVER=linux-5.14.2

get_and_prepare() {
    wget https://cdn.kernel.org/pub/linux/kernel/v5.x/$KERNELVER.tar.xz
    tar -xf $KERNELVER.tar.xz
    cp -r config $KERNELVER/.config
}


patch_kernel() {	
  for i in $(ls patches); do
     patch -Np1 -d $KERNELVER < patches/0001-amdgpu-clock.patch
  done
}

build() {
    export KBUILD_BUILD_HOST=archlinux
    export KBUILD_BUILD_USER=linux-amdclock
    cd $KERNELVER
    make -j10
    make modules -j10
    sudo cp -v arch/x86/boot/bzImage /boot/vmlinuz-linux-amdclock
    sudo make modules_install
}

if ! command -v wget &> /dev/null; then
    echo "Please install wget"
    exit 1
fi

case "$1" in
 -b|--build-only)
    build
    exit 0
    ;;
 -p|--patch-only)
    patch_kernel
    exit 0
    ;;
esac

get_and_prepare
patch_kernel
build
```

On each update you would have to increase the kernel version and recompile the new kernel to copy it to your bootdir.

Also, you would have to blacklist the `linux` package on your distribution's package manager so it doesn't automatically update and you don't lose the changes made.

In the case of Archlinux, as aaalwayss ;)) the wiki clearly explains it: [link](https://wiki.archlinux.org/title/Pacman#Skip_package_from_being_upgraded)

