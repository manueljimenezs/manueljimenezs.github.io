---
layout: post
title: "Enabling Screensaver from Spotlight search with AppleScript"
categories: how-to
date: 2021-04-24 13:19:54 +01:00
---

This is a useful way to lock your screen without actually installing any third-party software or having to map a new keystroke.

* Open Script Editor and put down this code:
  
  ```
  tell application "ScreenSaverEngine" to run
  ```

* Then select `File -> Export` on the menubar and choose: `Format: Application` save the app to your Applications folder.

Now you can trigger the screensaver from the search or having a shortcut on your dock.

![](/assets/img/2020-11-14-screensaver-script/spotlight-applescript.png){: .center-image }
