import os
import subprocess
import gdown
from flask import Flask

# Flask server
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ YouTube Stream is Running via Render!"

# 🔑 YouTube Stream Key
STREAM_KEY = "2c4f-5sy5-q7tx-cz4t-0c8r"

# 🎥 Google Drive File IDs
VIDEO_FILE_ID = "1-MJuCDwkcLmUuTTHVuRKqKVY1fCb2qm6"  # Video
AUDIO_FILE_ID = "1ilOvOl76gwquhWU-Xz78rcTOwLPdnizY"  # Music

VIDEO_FILE = "video.mp4"
AUDIO_FILE = "audio.mp3"

# 📥 Download video if not already present
if not os.path.exists(VIDEO_FILE):
    print("📥 Downloading video from Google Drive...")
    gdown.download(f"https://drive.google.com/uc?id={VIDEO_FILE_ID}", VIDEO_FILE, quiet=False)

# 📥 Download audio if not already present
if not os.path.exists(AUDIO_FILE):
    print("📥 Downloading audio from Google Drive...")
    gdown.download(f"https://drive.google.com/uc?id={AUDIO_FILE_ID}", AUDIO_FILE, quiet=False)

# ▶️ Start ffmpeg in background (loop video + audio, stream to YouTube)
ffmpeg_command = [
    "ffmpeg",
    "-stream_loop", "-1", "-i", VIDEO_FILE,
    "-stream_loop", "-1", "-i", AUDIO_FILE,
    "-c:v", "libx264",
    "-preset", "veryfast",
    "-b:v", "2500k",
    "-maxrate", "2500k",
    "-bufsize", "5000k",
    "-pix_fmt", "yuv420p",
    "-g", "50",
    "-c:a", "aac",
    "-b:a", "128k",
    "-ar", "44100",
    "-shortest",
    "-f", "flv",
    f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"
]

subprocess.Popen(ffmpeg_command)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render ke liye dynamic port
    app.run(host="0.0.0.0", port=port)
