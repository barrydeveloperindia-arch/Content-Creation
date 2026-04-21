import os
from cv_cropper import track_and_crop

def test_cropper():
    input_video = r"C:\Users\pc\Documents\Antigravity\Social Media Content Editor\opus_clone\Assets\IMG_9585.MOV"
    output_video = r"C:\Users\pc\Documents\Antigravity\Social Media Content Editor\opus_clone\temp_assets\IMG_9585_vertical.mp4"
    
    if not os.path.exists(input_video):
        print(f"Error: Could not find {input_video}")
        return
        
    print(f"Testing the Virtual Cameraman on {os.path.basename(input_video)}...")
    track_and_crop(input_video, output_video)
    
    print("\n--- TEST COMPLETE ---")
    print(f"Check out your new automatically reframed 9:16 vertical video here:\n{output_video}")

if __name__ == "__main__":
    test_cropper()
