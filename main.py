import os
import subprocess
import gdown
from flask import Flask

# ===== Flask Server =====
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ YouTube Stream is Running via Render!"

# ===== YouTube Stream Key =====
STREAM_KEY = "2c4f-5sy5-q7tx-cz4t-0c8r"  # Aapka stream key

# ===== Google Drive File IDs =====
VIDEO_FILE_ID = ""  # Video
AUDIO_FILE_ID = "1fO8xVEIKALIZAMMYcFEMQK4Rk0cFtBp6"  # Audio / Music

VIDEO_FILE = "video.mp4"
AUDIO_FILE = "audio.mp3"

# ===== Download video if not already present =====
if not os.path.exists(VIDEO_FILE):
    print("📥 Downloading video from Google Drive...")
    gdown.download(f"https://drive.google.com/uc?id={VIDEO_FILE_ID}", VIDEO_FILE, quiet=False)

# ===== Download audio if not already present =====
if not os.path.exists(AUDIO_FILE):
    print("📥 Downloading audio from Google Drive...")
    gdown.download(f"https://drive.google.com/uc?id={AUDIO_FILE_ID}", AUDIO_FILE, quiet=False)

# ===== Start FFmpeg for YouTube streaming (loop video + audio) =====
ffmpeg_command = [
    "ffmpeg",
    "-re",  # Real-time streaming
    "-stream_loop", "-1", "-i", VIDEO_FILE,  # Loop video infinitely
    "-stream_loop", "-1", "-i", AUDIO_FILE,  # Loop audio infinitely
    "-c:v", "libx264",
    "-preset", "veryfast",
    "-b:v", "4500k",         # Recommended video bitrate
    "-maxrate", "4500k",
    "-bufsize", "9000k",
    "-pix_fmt", "yuv420p",
    "-g", "60",              # Keyframe every 2 seconds (for 30fps)
    "-c:a", "aac",
    "-b:a", "128k",          # Recommended audio bitrate
    "-ar", "44100",
    "-f", "flv",
    f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"
]

# Start FFmpeg in background
subprocess.Popen(ffmpeg_command)

# ===== Flask App Run =====
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render ke liye dynamic port
    app.run(host="0.0.0.0", port=port)
