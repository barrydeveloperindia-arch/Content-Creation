import os
import glob
import json
import warnings
from ingestion import extract_audio, enhance_audio
from llm_engine import run_virality_engine

warnings.filterwarnings("ignore")

import imageio_ffmpeg
ffmpeg_path = os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe())
os.environ["PATH"] += os.pathsep + ffmpeg_path

def process_batch(assets_dir):
    print(f"Starting Batch Processor on directory: {assets_dir}")
    
    video_files = glob.glob(os.path.join(assets_dir, "*.MOV")) + glob.glob(os.path.join(assets_dir, "*.mp4"))
    
    if not video_files:
        print("No videos found in the Assets directory.")
        return

    print(f"Found {len(video_files)} videos. Beginning extraction pipeline...\n")
    
    try:
        import whisper
        print("Loading Whisper Base Model for batch transcription...")
        model = whisper.load_model("base")
    except ImportError:
        print("Whisper is not installed. Run: pip install openai-whisper")
        return

    all_batch_clips = []

    for index, video_path in enumerate(video_files):
        video_name = os.path.basename(video_path)
        print(f"\n[{index+1}/{len(video_files)}] Processing {video_name}...")
        
        try:
            # Phase 1
            print("  -> Extracting & Enhancing Audio...")
            audio_path = extract_audio(video_path, output_dir="temp_assets")
            enhanced_audio = enhance_audio(audio_path)
            
            # Phase 2
            print("  -> Transcribing...")
            result = model.transcribe(enhanced_audio, word_timestamps=True)
            transcript_file = enhanced_audio.replace(".wav", "_transcript.json")
            with open(transcript_file, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=4)
                
            # Phase 3
            print("  -> Running Gemini Virality Engine...")
            viral_clips_file = run_virality_engine(transcript_file)
            
            with open(viral_clips_file, "r", encoding="utf-8") as f:
                clips = json.load(f)
                
            for clip in clips:
                clip["source_video"] = video_name
                all_batch_clips.append(clip)
                
            print(f"  -> Found {len(clips)} potential clips in {video_name}.")
            
        except Exception as e:
            print(f"  -> ERROR processing {video_name}: {e}")

    # Final aggregation
    all_batch_clips.sort(key=lambda x: x.get("virality_score", 0), reverse=True)
    
    master_file = "MASTER_ENGLABS_CLIPS.json"
    with open(master_file, "w", encoding="utf-8") as f:
        json.dump(all_batch_clips, f, indent=4)
        
    print("\n--- BATCH PROCESSING COMPLETE ---")
    print(f"Successfully processed {len(video_files)} videos.")
    print(f"Generated a total of {len(all_batch_clips)} viral clips across all footage.")
    print(f"Review the master calendar here: {master_file}")

if __name__ == "__main__":
    # If API key isn't set, try grabbing GOOGLE_API_KEY from environment
    if not os.environ.get("GEMINI_API_KEY"):
        os.environ["GEMINI_API_KEY"] = os.environ.get("GOOGLE_API_KEY", "")
        
    assets_folder = r"C:\Users\pc\Documents\Antigravity\Social Media Content Editor\opus_clone\Assets"
    process_batch(assets_folder)
