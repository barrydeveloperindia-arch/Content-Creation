import os
import json
import warnings
warnings.filterwarnings("ignore")

try:
    from google import genai
except ImportError:
    pass

def generate_seo(context="Englabs manufacturing start-to-finish powder coating workflow montage"):
    """
    Phase 7: SEO & Metadata Generator
    Uses Google Gemini to write highly-converting, algorithm-friendly titles, descriptions, and hashtags.
    """
    print("\n--- PHASE 7: ENGLABS AI SEO GENERATOR ---")
    
    api_key = os.environ.get("GEMINI_API_KEY", os.environ.get("GOOGLE_API_KEY", ""))
    
    if not api_key:
        print("Warning: No GEMINI_API_KEY found in environment variables. Using optimized fallback SEO.")
        return _fallback_seo()
        
    try:
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        You are an expert Social Media Manager for a high-end manufacturing company called 'Englabs'.
        We just generated a fast-paced, highly satisfying short-form video montage of our process.
        
        Context of the video: {context}
        
        Generate the SEO metadata for Instagram Reels and TikTok.
        Follow these exact rules:
        1. TITLE: One punchy, highly-retaining hook.
        2. DESCRIPTION: 2-3 short sentences. Sound professional but natively "TikTok/Instagram" (use emojis).
        3. HASHTAGS: Provide exactly 8 highly relevant hashtags (mix of broad and niche, like #powdercoating, #manufacturing).
        
        Output EXACTLY in JSON format with keys: "title", "description", "hashtags" (list of strings).
        Do NOT wrap the output in markdown code blocks, just raw JSON.
        """
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        text = response.text.replace("```json", "").replace("```", "").strip()
        seo_data = json.loads(text)
        
        return seo_data
        
    except Exception as e:
        print(f"Error calling Gemini for SEO: {e}")
        return _fallback_seo()

def _fallback_seo():
    return {
        "title": "Wait for the final finish...",
        "description": "Start-to-finish inside the Englabs factory floor. From raw parts to a flawless powder coat, this is how we build premium hardware.",
        "hashtags": ["#manufacturing", "#powdercoating", "#engineering", "#oddlysatisfying", "#howitsmade", "#englabs", "#factory", "#industrial"]
    }

if __name__ == "__main__":
    seo = generate_seo()
    
    print("\n[ VIRAL METADATA GENERATED ]\n")
    print(f"TITLE: {seo.get('title')}")
    print(f"DESC:  {seo.get('description')}")
    print(f"TAGS:  {' '.join(seo.get('hashtags', []))}")
    
    # Save to file so the Auto-Publisher can read it
    output_file = "temp_assets/MONTAGE_SEO.json"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(seo, f, indent=4)
    print(f"\nSaved SEO data for the Auto-Publisher at {output_file}")
