# Memorial Montage Video Generator 🎞️🕊️

A Flask-based web application that generates a **1-minute memorial montage video** for a deceased loved one.  
The app takes **user-uploaded images, background music, and a Bible verse**, then produces a meaningful tribute video with text overlays.

---

## ✨ Features

- Upload **4 images** of the deceased
- Upload background **music**
- Add a **Bible verse or custom text**
- Automatically generates a **1-minute memorial video**
- Image transitions and text overlays
- Simple and clean web interface

---

## 🛠️ Tech Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS
- **Video Processing:** MoviePy
- **Image Processing:** Pillow (PIL)
- **Numerical Operations:** NumPy

---

## 📦 Python Packages Used

```python
from flask import Flask, render_template, request, send_from_directory
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from textwrap import wrap
from moviepy.editor import (
    ImageClip,
    concatenate_videoclips,
    AudioFileClip,
    TextClip,
    CompositeVideoClip,
    VideoClip
)
import os
import shutil
