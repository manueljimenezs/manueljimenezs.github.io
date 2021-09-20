#!/usr/bin/env python3

import datetime
import os
import re
title = input("Post title: ")
today = datetime.date.today()

skel = """---
layout: post
title: {0}
date: {1}
categories:
---""".format(title,today)

title_slug = re.sub('[^a-zA-Z -]+', '',title).replace(' ','-').lower()
path = "../_posts/"+str(today)+"-"+title_slug+".md"
with open(path, "w") as f:
    f.write(skel)
    
print("New post created at: "+path)
