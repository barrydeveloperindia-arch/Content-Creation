import os
import subprocess
try:
    import yt_dlp
except ImportError:
    print("yt_dlp not installed. Run: pip install yt-dlp")
    yt_dlp = None

def download_youtube_video(url, output_dir="temp_assets"):
    """
    Task 1.1: Source Downloader
    Downloads the best quality MP4 from a YouTube URL.
    """
    if not yt_dlp:
        raise ImportError("yt_dlp is required to download videos.")
        
    os.makedirs(output_dir, exist_ok=True)
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': os.path.join(output_dir, '%(id)s.%(ext)s'),
    }
    
    print(f"Downloading {url}...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_id = info_dict.get("id", "video")
        ext = info_dict.get("ext", "mp4")
        return os.path.join(output_dir, f"{video_id}.{ext}")

def extract_audio(video_path, output_dir="temp_assets"):
    """
    Task 1.2: Audio Extraction
    Extracts audio from the video file to WAV format using FFmpeg.
    """
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.basename(video_path).split('.')[0]
    audio_path = os.path.join(output_dir, f"{base_name}.wav")
    
    import imageio_ffmpeg
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    
    # FFmpeg command to extract audio: -vn (no video), -acodec pcm_s16le (standard wav), -ar 16000 (16kHz for whisper)
    command = [
        ffmpeg_exe, "-y", "-i", video_path, 
        "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", 
        audio_path
    ]
    
    print(f"Extracting audio to {audio_path}...")
    try:
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return audio_path
    except FileNotFoundError:
        raise RuntimeError("FFmpeg is not installed or not in PATH. Please install FFmpeg.")

def enhance_audio(audio_path):
    """
    Task 1.3: Audio Enhancement
    Normalizes audio levels using FFmpeg's loudnorm filter.
    """
    enhanced_audio_path = audio_path.replace(".wav", "_enhanced.wav")
    
    import imageio_ffmpeg
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    
    # Using ffmpeg's loudnorm filter for basic normalization
    command = [
        ffmpeg_exe, "-y", "-i", audio_path,
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
        enhanced_audio_path
    ]
    
    print(f"Enhancing audio to {enhanced_audio_path}...")
    subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return enhanced_audio_path

if __name__ == "__main__":
    print("Phase 1: Ingestion & Pre-Processing Module Ready.")
    # Example Usage:
    # url = "YOUR_YOUTUBE_URL_HERE"
    # video_file = download_youtube_video(url)
    # audio_file = extract_audio(video_file)
    # final_audio = enhance_audio(audio_file)
    # print(f"Processing complete. Audio ready for transcription: {final_audio}")
