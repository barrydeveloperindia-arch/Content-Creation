import warnings
warnings.filterwarnings("ignore")
import whisper
import numpy as np
import scipy.io.wavfile as wav

print("Loading Whisper...")
model = whisper.load_model("base")

audio_path = r"C:\Users\pc\Documents\Antigravity\Social Media Content Editor\opus_clone\temp_assets\IMG_9585.wav"
print(f"Reading {audio_path}...")

# Read wav file using scipy to completely bypass the internal ffmpeg crash
sample_rate, data = wav.read(audio_path)

# Convert to float32 between -1 and 1
if data.dtype == np.int16:
    data = data.astype(np.float32) / 32768.0

# If stereo, convert to mono
if len(data.shape) > 1:
    data = data.mean(axis=1)

# Whisper expects exactly 16000 Hz. If it's not, we just pass it (ingestion.py converted it to 16000 already)
print("Transcribing actual audio...")
result = model.transcribe(data)

print("\n--- ACTUAL TRANSCRIPT ---")
print(result["text"])
