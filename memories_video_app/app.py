from flask import Flask, render_template, request, send_from_directory
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from textwrap import wrap
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip, TextClip, CompositeVideoClip, VideoClip
import os
import shutil

app = Flask(__name__)

PHOTO_FOLDER = "uploads/photos"
MUSIC_FOLDER = "uploads/music"
OUTPUT_FOLDER = "static/generated"
OUTPUT_VIDEO = "memories_video.mp4"

MAX_PHOTOS = 10
MAX_DURATION = 60

# Ensure folders exist
os.makedirs(PHOTO_FOLDER, exist_ok=True)
os.makedirs(MUSIC_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # Clear old files
        shutil.rmtree(PHOTO_FOLDER)
        shutil.rmtree(MUSIC_FOLDER)
        os.makedirs(PHOTO_FOLDER)
        os.makedirs(MUSIC_FOLDER)

        # Save photos
        photos = request.files.getlist("photos")
        photos = photos[:MAX_PHOTOS]

        for photo in photos:
            photo.save(os.path.join(PHOTO_FOLDER, photo.filename))

        # Save music
        music = request.files["music"]
        music_path = os.path.join(MUSIC_FOLDER, music.filename)
        music.save(music_path)

        memorial_text = request.form.get("memorial_text", "").strip()

        # -------- VIDEO GENERATION --------
        photo_files = [
            os.path.join(PHOTO_FOLDER, f)
            for f in os.listdir(PHOTO_FOLDER)
            if f.lower().endswith(('.jpg', '.png', '.jpeg'))
        ]

        num_photos = len(photo_files)
        photo_duration = MAX_DURATION / num_photos

        clips = []
        for photo in photo_files:
            clip = ImageClip(photo).set_duration(photo_duration)
            clip = clip.fadein(1).fadeout(1)
            clips.append(clip)


        video = concatenate_videoclips(clips, method="compose")

        if memorial_text:
            text_overlay = create_text_overlay(
                memorial_text,
                video.size,
                video.duration
            )
            video = CompositeVideoClip([video, text_overlay])



        audio = AudioFileClip(music_path).set_duration(video.duration)
        video = video.set_audio(audio)

        output_path = os.path.join(OUTPUT_FOLDER, OUTPUT_VIDEO)
        video.write_videofile(output_path, fps=24)

        return render_template("index.html", video_generated=True)

    return render_template("index.html", video_generated=False)

def create_text_overlay(text, video_size, duration):
    W, H = video_size
    max_chars_per_line = 32  # controls wrapping

    lines = wrap(text, max_chars_per_line)

    font_path = "C:/Windows/Fonts/times.ttf"
    font_size = 42

    def make_frame(t):
        img = Image.new("RGB", (W, H), (0, 0, 0))
        draw = ImageDraw.Draw(img)

        font = ImageFont.truetype(font_path, font_size)

        total_height = 0
        line_heights = []

        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            h = bbox[3] - bbox[1]
            line_heights.append(h)
            total_height += h + 10

        # 🔼 Move text higher
        y = H - total_height - 160

        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (W - text_width) // 2

            draw.text((x, y), line, fill=(255, 255, 255), font=font)
            y += line_heights[i] + 10

        return np.array(img)

    def make_mask(t):
        mask = Image.new("L", (W, H), 0)
        draw = ImageDraw.Draw(mask)

        font = ImageFont.truetype(font_path, font_size)

        total_height = 0
        line_heights = []

        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            h = bbox[3] - bbox[1]
            line_heights.append(h)
            total_height += h + 10

        y = H - total_height - 160

        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (W - text_width) // 2

            draw.text((x, y), line, fill=255, font=font)
            y += line_heights[i] + 10

        return np.array(mask) / 255.0

    text_clip = VideoClip(make_frame, duration=duration)
    mask_clip = VideoClip(make_mask, ismask=True, duration=duration)

    return text_clip.set_mask(mask_clip)




@app.route("/download")
def download():
    return send_from_directory(OUTPUT_FOLDER, OUTPUT_VIDEO, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
