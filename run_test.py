import os
import json
import warnings
from ingestion import extract_audio, enhance_audio
from llm_engine import run_virality_engine

# Ignore warnings from PyTorch/Whisper for cleaner output
warnings.filterwarnings("ignore")

def test():
    import imageio_ffmpeg
    ffmpeg_path = os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe())
    os.environ["PATH"] += os.pathsep + ffmpeg_path
    
    video_path = r"C:\Users\pc\Documents\Antigravity\Social Media Content Editor\opus_clone\Assets\IMG_9584.MOV"
    if not os.path.exists(video_path):
        print(f"Error: Could not find {video_path}")
        return

    print(f"Testing pipeline on {os.path.basename(video_path)}")
    
    # Phase 1
    print("\n[Phase 1] Extracting & Enhancing Audio...")
    audio_path = extract_audio(video_path, output_dir="temp_assets")
    enhanced_audio = enhance_audio(audio_path)
    
    # Phase 2
    print("\n[Phase 2] Running Transcription (using Whisper Base Model)...")
    try:
        import whisper
    except ImportError:
        print("Whisper is still installing. Please wait a moment and try again.")
        return
        
    # We use 'base' for a fast test. In production, we'd use 'large' or 'turbo'.
    model = whisper.load_model("base") 
    result = model.transcribe(enhanced_audio, word_timestamps=True)
    
    transcript_file = enhanced_audio.replace(".wav", "_transcript.json")
    with open(transcript_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)
        
    print(f"Transcription saved to {transcript_file}")
        
    # Phase 3
    print("\n[Phase 3] Running Gemini Virality Engine...")
    try:
        viral_clips_file = run_virality_engine(transcript_file)
        print("\n--- TEST COMPLETE ---")
        print(f"Viral Clips suggested by Gemini have been saved to: {viral_clips_file}")
        
        # Print out the results for the user to see!
        with open(viral_clips_file, "r", encoding="utf-8") as f:
            clips = json.load(f)
            if not clips:
                print("Gemini didn't find any clips it thought were viral enough (score > 0).")
            else:
                print("\nTOP VIRAL CLIPS FOUND:")
                for i, clip in enumerate(clips):
                    print(f"\nClip {i+1}: {clip.get('title', 'Untitled')}")
                    print(f"Score: {clip.get('virality_score', 'N/A')}/99")
                    print(f"Reasoning: {clip.get('reasoning', 'N/A')}")
    except Exception as e:
        print(f"Phase 3 Failed: {e}")

if __name__ == "__main__":
    test()
