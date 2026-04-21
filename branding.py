import os
import warnings

# Suppress moviepy welcome message
os.environ["IMAGEIO_USERDIR"] = "true" 
warnings.filterwarnings("ignore")

from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

def apply_watermark(video_path, logo_path, output_path, position=("right", "top"), opacity=0.85):
    """
    Phase 6: Branding & Watermarking
    Overlays the Englabs logo onto the vertical video, positioned perfectly to avoid TikTok/Reels UI.
    """
    print(f"Applying Englabs branding to {os.path.basename(video_path)}...")
    
    if not os.path.exists(video_path):
        print(f"Error: Video file not found at {video_path}")
        return
        
    if not os.path.exists(logo_path):
        print(f"Warning: Logo not found at {logo_path}. Cannot apply watermark.")
        return

    video = VideoFileClip(video_path)
    
    # Load the logo
    logo = ImageClip(logo_path)
    
    # Resize logo dynamically based on video width (e.g., 20% of the screen width for 9:16 video)
    # This ensures it looks the same on a 1080p output as a 4K output
    target_width = int(video.w * 0.25)
    logo = logo.resize(width=target_width)
    
    # Apply opacity to make it look premium
    logo = logo.set_opacity(opacity)
    
    # Set position (margin of 40 pixels)
    if position == ("right", "top"):
        # Custom placement with 40px margin from top and right
        logo = logo.set_position(lambda t: (video.w - logo.w - 40, 40))
    elif position == ("center", "top"):
        logo = logo.set_position(("center", 40))
    else:
        logo = logo.set_position(position)
        
    # The logo stays on screen for the entire duration of the video
    logo = logo.set_duration(video.duration)
    
    # Composite the logo over the video
    final = CompositeVideoClip([video, logo])
    
    print(f"Exporting fully branded video to {output_path}...")
    final.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=video.fps, logger="bar")
    
    print("Branding complete!")
    return output_path

if __name__ == "__main__":
    print("Phase 6: Branding Module Ready.")
