from gtts import gTTS
import subprocess
import os

# === CONFIGURATION ===
STORY_FILE = "story.txt"
VOICE_FILE = "voice.mp3"
SRT_FILE = "voice.srt"
WHISPER_MODEL = "base"  # or 'small', 'medium', etc.

def generate_voice():
    if not os.path.exists(STORY_FILE):
        raise FileNotFoundError("❌ 'story.txt' not found!")

    with open(STORY_FILE, "r", encoding="utf-8") as f:
        story_text = f.read().strip()

    if not story_text:
        raise ValueError("❌ 'story.txt' is empty!")

    print("🔊 Generating voice.mp3 from story.txt...")
    tts = gTTS(story_text)
    tts.save(VOICE_FILE)
    print(f"✅ Saved voiceover to '{VOICE_FILE}'")

def generate_subtitles():
    print("📝 Transcribing voice.mp3 with Whisper to generate subtitles...")
    subprocess.run([
        "whisper",
        VOICE_FILE,
        "--model", WHISPER_MODEL,
        "--output_format", "srt"
    ], check=True)

    if os.path.exists("voice.srt"):
        print(f"✅ Subtitle file created: {SRT_FILE}")
    else:
        raise RuntimeError("❌ Whisper failed to generate subtitle file.")

def main():
    generate_voice()
    generate_subtitles()

if __name__ == "__main__":
    main()
