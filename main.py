import os
import subprocess
import gdown

# 🔑 Apna YouTube Stream Key daalo
STREAM_KEY = "2c4f-5sy5-q7tx-cz4t-0c8r"

# 📥 Google Drive se apne file IDs daalo
VIDEO_FILE_ID = "1-MJuCDwkcLmUuTTHVuRKqKVY1fCb2qm6"  # e.g. mp4
AUDIO_FILE_ID = "1ilOvOl76gwquhWU-Xz78rcTOwLPdnizY"  # e.g. mp3

# Output file names
VIDEO_FILE = "video.mp4"
AUDIO_FILE = "audio.mp3"

# Download video if not present
if not os.path.exists(VIDEO_FILE):
    print("📥 Downloading video from Google Drive...")
    gdown.download(f"https://drive.google.com/uc?id={VIDEO_FILE_ID}", VIDEO_FILE, quiet=False)

# Download audio if not present
if not os.path.exists(AUDIO_FILE):
    print("📥 Downloading audio from Google Drive...")
    gdown.download(f"https://drive.google.com/uc?id={AUDIO_FILE_ID}", AUDIO_FILE, quiet=False)

# ffmpeg command (video + audio, both looped)
command = [
    "ffmpeg",
    "-stream_loop", "-1", "-i", VIDEO_FILE,   # loop video
    "-stream_loop", "-1", "-i", AUDIO_FILE,   # loop audio
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
    "-shortest",  # dono loop ke saath sync karega
    "-f", "flv",
    f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"
]

# Run ffmpeg
subprocess.run(command)
