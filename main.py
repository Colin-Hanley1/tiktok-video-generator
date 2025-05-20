import os
import random
import subprocess
import json
from gtts import gTTS

# === CONFIGURATION ===
BACKGROUND_FOLDER = "backgrounds"
STORY_FILE = "story.txt"
VOICE_MP3 = "voice.mp3"
SUBTITLE_FILE = "voice.srt"
TITLE_CARD_IMAGE = "title_card.png"
FINAL_VIDEO = "output.mp4"

# === UTILS ===

def choose_random_video(folder):
    videos = [f for f in os.listdir(folder) if f.endswith((".mp4", ".mov", ".mkv"))]
    if not videos:
        raise FileNotFoundError(f"No video files found in {folder}")
    return os.path.join(folder, random.choice(videos))

def get_audio_duration(path):
    result = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "json", path
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return float(json.loads(result.stdout)["format"]["duration"])

def generate_voice(text, output_path):
    print("🔊 Generating voiceover from story.txt...")
    tts = gTTS(text)
    tts.save(output_path)

def extend_video_to_duration(input_path, output_path, duration):
    print(f"⏳ Extending background to {duration:.2f} seconds...")
    subprocess.run([
        "ffmpeg", "-y",
        "-stream_loop", "-1",
        "-i", input_path,
        "-t", str(duration),
        "-c:v", "libx264",
        "-an",
        output_path
    ], check=True)

def build_video(video_path, audio_path, subtitle_path, overlay_image_path, output_path, duration):
    print(f"🎞️ Creating final video with subtitles: {output_path}")

    filter_str = (
        "[0:v]scale=1080:1920:force_original_aspect_ratio=decrease,"
        "pad=1080:1920:(ow-iw)/2:(oh-ih)/2[base];"
        "[1:v]format=rgba[img];"
        "[base][img]overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/5[bg];"
        f"[bg]subtitles={subtitle_path}:force_style='Alignment=6\\,FontName=Open Sans\\,FontSize=18\\,Outline=1\\,Shadow=1\\,MarginV=120'[vout]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", overlay_image_path,
        "-i", audio_path,
        "-filter_complex", filter_str,
        "-map", "[vout]", "-map", "2:a:0",
        "-t", str(duration),  # Ensure final video matches audio length
        "-c:v", "libx264", "-c:a", "aac",
        "-b:a", "192k", "-ar", "44100", "-ac", "2",
        output_path
    ]

    subprocess.run(cmd, check=True)

# === MAIN ===

def main():
    if not os.path.exists(STORY_FILE):
        raise FileNotFoundError("❌ Missing 'story.txt'!")
    if not os.path.exists(TITLE_CARD_IMAGE):
        raise FileNotFoundError(f"❌ Missing title card image: {TITLE_CARD_IMAGE}")
    if not os.path.exists(SUBTITLE_FILE):
        raise FileNotFoundError(f"❌ Missing subtitle file: {SUBTITLE_FILE}")

    with open(STORY_FILE, "r", encoding="utf-8") as f:
        story_text = f.read().strip()


    background_video = choose_random_video(BACKGROUND_FOLDER)
    print("🎥 Selected background video:", background_video)

    duration = get_audio_duration(VOICE_MP3)
    print(f"🎧 Total voice duration: {duration:.2f}s")

    extend_video_to_duration(background_video, "looped_background.mp4", duration)

    build_video(
        video_path="looped_background.mp4",
        audio_path=VOICE_MP3,
        subtitle_path=SUBTITLE_FILE,
        overlay_image_path=TITLE_CARD_IMAGE,
        output_path=FINAL_VIDEO,
        duration=duration
    )

    print(f"✅ Done! Final video saved as: {FINAL_VIDEO}")

if __name__ == "__main__":
    main()
