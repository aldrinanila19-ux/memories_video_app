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



🚀 How It Works

User uploads:

images(max 10)

1 music file

A Bible verse or memorial text

Images are processed and resized using PIL

Text is wrapped and overlaid on images

Video clips are created using MoviePy

Background music is synced

▶️ How to Run the Project
1️⃣ Clone the Repository
git clone https://github.com/USERNAME/REPO_NAME.git
cd REPO_NAME

2️⃣ Create Virtual Environment (Recommended)
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

3️⃣ Install Dependencies
pip install flask pillow moviepy numpy

4️⃣ Run the Application
python app.py

5️⃣ Open in Browser
http://127.0.0.1:5000/A 1-minute montage video is generated and saved
