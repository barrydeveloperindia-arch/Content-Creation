import os
import json
try:
    import whisperx
except ImportError:
    print("whisperx not installed. Please install it to run transcription.")
    whisperx = None

def run_transcription(audio_file, hf_token=None, device="cpu", compute_type="int8"):
    """
    Task 2.1 & 2.2: Word-Level Transcription & Speaker Diarization
    Uses WhisperX to get word-level timestamps and speaker mapping.
    
    Note: Speaker diarization requires a HuggingFace token (hf_token) 
    and agreeing to pyannote's terms of service on HuggingFace.
    """
    if not whisperx:
        raise ImportError("whisperx is required.")
        
    print(f"Loading WhisperX model on {device}...")
    # Load model (using 'base' for faster testing, use 'large-v2' for production accuracy)
    model = whisperx.load_model("base", device, compute_type=compute_type)
    
    print("Transcribing audio...")
    audio = whisperx.load_audio(audio_file)
    result = model.transcribe(audio, batch_size=16)
    
    print("Aligning timestamps to word-level...")
    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
    result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)
    
    if hf_token:
        print("Running speaker diarization...")
        diarize_model = whisperx.DiarizationPipeline(use_auth_token=hf_token, device=device)
        diarize_segments = diarize_model(audio)
        result = whisperx.assign_word_speakers(diarize_segments, result)
    else:
        print("Skipping diarization (no HuggingFace token provided).")
        
    # Save the output to a JSON file
    output_file = audio_file.replace(".wav", "_transcript.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4)
        
    print(f"Transcription saved to {output_file}")
    return output_file

def detect_filler_words(json_transcript_path):
    """
    Task 2.3: Filler Word Detection
    Parses the JSON and flags 'um', 'uh', and long pauses.
    """
    with open(json_transcript_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    filler_words = ["um", "uh", "like", "you know"]
    flagged_timestamps = []
    
    for segment in data.get("segments", []):
        for word_info in segment.get("words", []):
            word_text = word_info.get("word", "").lower().strip(".,!?")
            if word_text in filler_words and "start" in word_info and "end" in word_info:
                flagged_timestamps.append({
                    "word": word_text,
                    "start": word_info["start"],
                    "end": word_info["end"]
                })
                
    # Output the flagged filler words
    filler_file = json_transcript_path.replace("_transcript.json", "_fillers.json")
    with open(filler_file, 'w', encoding='utf-8') as f:
        json.dump(flagged_timestamps, f, indent=4)
        
    print(f"Detected {len(flagged_timestamps)} filler words. Saved to {filler_file}")
    return filler_file

if __name__ == "__main__":
    print("Phase 2: Transcription & Diarization Module Ready.")
    # Example Usage:
    # audio_path = "temp_assets/video_enhanced.wav"
    # transcript = run_transcription(audio_path, hf_token="YOUR_HF_TOKEN")
    # detect_filler_words(transcript)
