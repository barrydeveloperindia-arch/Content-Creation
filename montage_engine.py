import os
import glob
from moviepy.editor import VideoFileClip, ImageClip, ColorClip, CompositeVideoClip, concatenate_videoclips
import moviepy.video.fx.all as vfx
import warnings
from branding import apply_watermark
from caption_engine import create_text_image

os.environ["IMAGEIO_USERDIR"] = "true" 
warnings.filterwarnings("ignore")

def create_masterpiece_montage(assets_dir, output_path):
    print("\n--- REBUILDING V4 MASTERPIECE (INTRO/OUTRO & LOUD LABELS) ---")
    
    video_files = glob.glob(os.path.join(assets_dir, "*.MOV")) + glob.glob(os.path.join(assets_dir, "*.mp4"))
    video_files.sort() 
    
    if not video_files:
        print("Error: No videos found in Assets directory.")
        return
        
    clips = []
    
    for vid in video_files:
        try:
            clip = VideoFileClip(vid)
            
            # High-Res 9:16 Cropping using MoviePy's native FFmpeg engine
            target_width = int(clip.h * (9 / 16))
            if target_width % 2 != 0:
                target_width -= 1
                
            x_center = clip.w / 2
            y_center = clip.h / 2
            clip = vfx.crop(clip, x_center=x_center, y_center=y_center, width=target_width, height=clip.h)
            
            # Smooth Crossfade Transition (0.5s overlap)
            clip = clip.crossfadein(0.5)
            clip = clip.without_audio()
            clips.append(clip)
            
        except Exception as e:
            print(f"Skipping {os.path.basename(vid)} due to error: {e}")
            
    print(f"Stitching all {len(clips)} full-length clips...")
    master_vertical = concatenate_videoclips(clips, padding=-0.5, method="compose")
    
    # ---------------------------------------------------------
    # V4 UPGRADE: THE OUTRO
    # ---------------------------------------------------------
    print("Generating Englabs Outro Sequence...")
    logo_path = r"C:\Users\pc\OneDrive - Englabs India Pvt Ltd\Automate_trial_MANUFACTURE\Desktop\OLD DATA\ENGLABS-KARTIK\ENGLABS logo.png"
    
    # Create a 2-second black background
    outro_bg = ColorClip(size=master_vertical.size, color=(0,0,0)).set_duration(2.0)
    
    # Load and center the Englabs logo
    outro_logo = ImageClip(logo_path)
    outro_logo = outro_logo.resize(width=master_vertical.w * 0.5)
    outro_logo = outro_logo.set_position("center").set_duration(2.0)
    
    outro_clip = CompositeVideoClip([outro_bg, outro_logo]).set_duration(2.0).crossfadein(0.5)
    
    # Concatenate the master video with the outro
    final_timeline = concatenate_videoclips([master_vertical, outro_clip], padding=-0.5, method="compose")
    
    # ---------------------------------------------------------
    # V4 UPGRADE: THE INTRO "LOUD LABEL"
    # ---------------------------------------------------------
    print("Generating Loud Label (Hook)...")
    hook_text = "WAIT FOR THE FINAL FINISH"
    # Use our Pillow caption engine to generate a stunning text image (returns numpy array)
    text_img_array = create_text_image(hook_text, final_timeline.w, final_timeline.h, font_size=90, color="#FFD700")
    
    # Overlay the label for the first 3 seconds
    hook_clip = ImageClip(text_img_array)
    # Position it in the center
    hook_clip = hook_clip.set_position(("center", "center")).set_duration(3.0).crossfadeout(0.5)
    
    # Composite the label over the timeline
    final_composited = CompositeVideoClip([final_timeline, hook_clip])
    
    # ---------------------------------------------------------
    # RENDER & WATERMARK
    # ---------------------------------------------------------
    temp_vertical_path = "temp_assets/MASTER_MONTAGE_V4_RAW.mp4"
    
    print("Rendering high-resolution master file...")
    final_composited.write_videofile(
        temp_vertical_path, 
        codec="libx264", 
        audio_codec="aac", 
        fps=30, 
        bitrate="20000k", 
        preset="fast",    
        ffmpeg_params=["-pix_fmt", "yuv420p"],
        logger=None
    )
    
    # Free memory
    for c in clips:
        c.close()
    master_vertical.close()
    final_timeline.close()
    final_composited.close()
    
    print("Applying Final Englabs Branding...")
    apply_watermark(temp_vertical_path, logo_path, output_path)
    
    print("\n--- V4 MASTERPIECE COMPLETE ---")
    print(f"Your final video is ready at: {output_path}")

if __name__ == "__main__":
    assets_folder = r"C:\Users\pc\Documents\Antigravity\Social Media Content Editor\opus_clone\Assets"
    final_output = r"C:\Users\pc\Documents\Antigravity\Social Media Content Editor\opus_clone\ENGLABS_WORKFLOW_MONTAGE_V4.mp4"
    create_masterpiece_montage(assets_folder, final_output)
