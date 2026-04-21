import os
import json
try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Google GenAI python package not installed. Run: pip install google-genai")
    genai = None

def chunk_transcript(transcript_json_path, max_words=1500):
    """
    Task 3.1: Chunking & Context Windowing
    Splits a large transcript into manageable chunks so the LLM doesn't lose context.
    Returns a list of strings (chunks) with their respective start/end times.
    """
    with open(transcript_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    chunks = []
    current_chunk = ""
    current_word_count = 0
    chunk_start_time = 0.0

    # Iterating through WhisperX word-level output
    for segment in data.get("segments", []):
        for word_info in segment.get("words", []):
            if current_word_count == 0 and "start" in word_info:
                chunk_start_time = word_info["start"]

            word_text = word_info.get("word", "")
            current_chunk += word_text + " "
            current_word_count += 1

            # When chunk limit is reached, save it and reset
            if current_word_count >= max_words:
                chunk_end_time = word_info.get("end", chunk_start_time)
                chunks.append({
                    "start_time": chunk_start_time,
                    "end_time": chunk_end_time,
                    "text": current_chunk.strip()
                })
                current_chunk = ""
                current_word_count = 0

    # Add any remaining text as the last chunk
    if current_chunk:
        last_segment = data.get("segments", [{}])[-1]
        last_word = last_segment.get("words", [{}])[-1]
        chunk_end_time = last_word.get("end", chunk_start_time)
        chunks.append({
            "start_time": chunk_start_time,
            "end_time": chunk_end_time,
            "text": current_chunk.strip()
        })

    return chunks

def analyze_for_virality(chunk_data):
    """
    Task 3.2 & 3.3: Hook Detection & Virality Scoring using Gemini
    """
    if not genai:
        raise ImportError("google-genai package is required.")
        
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is missing.")

    client = genai.Client(api_key=api_key)

    system_prompt = """
    You are an expert social media manager and video editor for a high-end engineering and manufacturing brand (Englabs).
    Your goal is to find the most viral, engaging 30-60 second clips from the provided transcript.
    
    A viral manufacturing clip MUST have:
    1. A strong Hook (grabs attention, mentions a problem, a material, or a complex part).
    2. Context/Body ("Oddly Satisfying" technical explanation of a workflow, CAD design, or machining process).
    3. Payoff (The reveal of the final product, the solution to the engineering bottleneck, or a profound statement).

    Analyze the text and identify potential clips. Give each a Virality Score (1-99).
    You MUST output valid JSON only. Format exactly like this:
    {
      "clips": [
        {
          "title": "Short catchy title",
          "virality_score": 85,
          "hook_text": "The exact first 5 words of the clip",
          "payoff_text": "The exact last 5 words of the clip",
          "reasoning": "Why this works for social media"
        }
      ]
    }
    """

    print(f"Analyzing chunk ({chunk_data['start_time']}s to {chunk_data['end_time']}s)...")
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=f"Here is the transcript chunk:\n\n{chunk_data['text']}",
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            response_mime_type="application/json",
            temperature=0.7,
        ),
    )

    try:
        result = json.loads(response.text)
        return result.get("clips", [])
    except json.JSONDecodeError:
        print("Error: Gemini did not return valid JSON.")
        return []

def run_virality_engine(transcript_json_path):
    """Main orchestrator for Phase 3."""
    print("--- Starting Phase 3: Gemini Virality Engine ---")
    chunks = chunk_transcript(transcript_json_path)
    print(f"Transcript split into {len(chunks)} chunks.")
    
    all_clips = []
    for chunk in chunks:
        clips = analyze_for_virality(chunk)
        all_clips.extend(clips)
        
    # Sort clips by highest virality score
    all_clips.sort(key=lambda x: x.get("virality_score", 0), reverse=True)
    
    output_file = transcript_json_path.replace("_transcript.json", "_viral_clips.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_clips, f, indent=4)
        
    print(f"Gemini Virality Engine complete. Found {len(all_clips)} potential clips.")
    print(f"Results saved to {output_file}")
    return output_file

if __name__ == "__main__":
    print("Phase 3 (Gemini Version) Module Ready.")
    # Example Usage:
    # transcript_file = "temp_assets/video_enhanced_transcript.json"
    # os.environ["GEMINI_API_KEY"] = "AIza..." 
    # run_virality_engine(transcript_file)
