import os
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Suppress moviepy welcome message
os.environ["IMAGEIO_USERDIR"] = "true" 
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

def create_text_image(text, width, height, font_size=120, color="white", stroke_color="black"):
    """
    Generates an image containing the text. 
    We use Pillow instead of MoviePy's TextClip to completely avoid ImageMagick installation errors on Windows!
    """
    # Create a transparent image
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Try to load a bold Windows font (Impact is great for Hormozi style), fallback to default
    try:
        font = ImageFont.truetype("impact.ttf", font_size)
    except IOError:
        try:
            font = ImageFont.truetype("arialbd.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

    # Calculate text size and position to center it
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    
    x = (width - text_w) / 2
    # Position slightly below the center (perfect for TikTok/Reels)
    y = (height - text_h) / 2 + 200 
    
    # Draw a thick stroke (outline) for readability
    stroke_width = 6
    for dx in range(-stroke_width, stroke_width+1, 2):
        for dy in range(-stroke_width, stroke_width+1, 2):
            draw.text((x+dx, y+dy), text, font=font, fill=stroke_color)
            
    # Draw the main text
    draw.text((x, y), text, font=font, fill=color)
    
    return np.array(img)

def render_captions(video_path, transcript_json, output_path):
    """
    Phase 5: Karaoke Caption Renderer
    Reads Whisper word-level timestamps and burns Hormozi-style fast captions onto the video.
    """
    print(f"Rendering captions for {os.path.basename(video_path)}...")
    video = VideoFileClip(video_path)
    
    if not os.path.exists(transcript_json):
        print(f"Error: Transcript not found at {transcript_json}")
        return
        
    with open(transcript_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    word_clips = []
    
    # Iterate through every single word in the Whisper transcript
    for segment in data.get("segments", []):
        for word_info in segment.get("words", []):
            word_text = word_info.get("word", "").strip()
            start_time = word_info.get("start", 0)
            end_time = word_info.get("end", start_time + 0.5)
            
            # Hormozi Style Rules: 
            # 1. Everything uppercase
            word_text = word_text.upper()
            
            # 2. Dynamic Highlighting (Highlight words longer than 5 letters in Englabs Yellow/Orange)
            # You can replace this with Englabs specific hex codes later!
            color = "#FFD700" if len(word_text) >= 5 else "white"
            
            # Generate the text graphic
            text_img_array = create_text_image(word_text, video.w, video.h, font_size=110, color=color)
            
            # Convert to a MoviePy ImageClip
            txt_clip = ImageClip(text_img_array)
            txt_clip = txt_clip.set_start(start_time).set_end(end_time)
            
            word_clips.append(txt_clip)
            
    # Overlay all the rapid-fire word clips onto the main video
    final_video = CompositeVideoClip([video] + word_clips)
    
    print(f"Exporting final captioned video to {output_path}...")
    # Render! We use libx264 for high compatibility with Instagram/YouTube Shorts
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=video.fps, logger="bar")
    
    print("Caption rendering complete!")
    return output_path

if __name__ == "__main__":
    print("Phase 5: Karaoke Caption Renderer Ready.")
    # Example usage:
    # render_captions("temp_assets/IMG_9585_vertical.mp4", "temp_assets/IMG_9585_transcript.json", "FINAL_READY_TO_POST.mp4")
