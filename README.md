# 🎬 TikTok Video Generator

This tool turns a short script (story or educational content) into a fully narrated, subtitled, TikTok-ready video. It supports auto-generated voiceover, subtitles, looping background, and title card overlays — all completely offline.

---

## 📁 Folder Structure

```bash
tiktok-video-generator/
├── main.py                # Main pipeline: builds video
├── subtitles.py           # Optional: generate subs.srt from voice.mp3 using whisper.cpp
├── story.txt              # Your input script
├── voice.mp3              # Auto-generated from story.txt using gTTS
├── subs.srt               # Optional subtitles in SRT format
├── title_card.png         # Overlay title card (1080x1920 recommended)
├── backgrounds/           # Folder with background .mp4 or .mov clips
│   ├── math_grid.mp4
│   └── blurry_lights.mov
├── requirements.txt       # Python dependencies
└── output.mp4             # Final rendered video
