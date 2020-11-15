---
layout: post
title: "A better terminal experience in macOS"
categories: guides
date: 2020-11-14 13:19:54 +01:00
---

 ![](/assets/img/2020-11-14-mac-terminal/neofetch.png){: .center-image }



## iTerm2: A superpowered terminal

iTerm2 provides enhancements to the terminal such as pasting on middle click or themes. you can download it [here](https://www.iterm2.com/)

## ZSH: Completion

From macOS Catalina, Apple changed the default shell from bash to zsh. With zsh, you can then install oh-my-zsh, which provides support for auto-completion, git or aws.

To change the default shell to zsh:

```
$ chsh -s /bin/zsh
```

Then [install](https://ohmyz.sh/#install) oh my zsh

### Customizing zsh

In mac, edit `.zshrc` and add as the first line:

```
ZSH_DISABLE_COMPFIX="true"
```

I also set _agnoster_ as the zsh theme (it's the theme shown on the pictures)

```
ZSH_THEME="agnoster"
```

You can also cusomize the themes to your liking, copy an existing theme to `.oh/my/zsh/custom/themes`. For example, if you want to only show the last two levels on the path, add a '2'after de '%'symbol:

```
prompt_dir() {
  prompt_segment blue $CURRENT_FG '%2~'
}
```

## brew: the package manager for macOS

This is a must when doing work on the terminal, this way you can install packages such as `tmux`, `python3`, `ffmpeg`. You only need to type `brew install <package name>`.

You can install it from one command, as shown [here](https://brew.sh).

