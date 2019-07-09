---
layout: post
title:  "FFmpeg, the video Swiss Army Knife"
date:   2019-01-24 10:55:30 +01:00
categories: tips
---

You may have found yourself in a situation where you have to modify a video or extract its audio. Firing up a complete editor for such simple tasks could be a waste of energy and time.

Here are some basic tips for FFmpeg that can sometimes make your workflow more efficient:

## Change the aspect ratio of a video without reencoding

This can be useful when the only thing we want to do is changing the proportions of a video without losing quality.

For example for converting a 4:3 video to an stretched 16:9:

```bash
ffmpeg -i in.mp4 -aspect 16:9 -c copy out.mp4
```

![4:3 to 16:9](/assets/img/ffmpeg_aspect.png)

The `-c copy` option allows setting up the codec to a copy mode where ffmpeg doesn't reencode the video and the results are done immediately.

## Extracting audio from a file

```bash
ffmpeg -i in.mp4 out.mp3
```

**Note:** the extensions shown here are completely arbitrary, ffmpeg supports a wide variety of codecs and formats which can be seen with the commands `ffmpeg -codecs` and `ffmpeg -formats`

## Cutting a video file without reencoding

```bash
ffmpeg -i in.mp4 -ss 00:00:25.0 -codec copy -t 30 out.mp4
```

_In this case the cut starts on second 25 and the video lasts 30 seconds_

## Converting a video to other format

```bash
ffmpeg -i in.ogv -c:v libx264 out.mp4
```

* `-c:v libx264` sets the video codec
* `-c:a vorbis` sets the audio codec
* `-r 25` sets the framerate to 25fps
* `-s <1280x720|hd720>` sets the video resolution to 720p
* `-b:v 1M` sets the _video_ bitrate to 1MB/s

