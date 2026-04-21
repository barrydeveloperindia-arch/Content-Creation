import os
import glob
import cv2
import warnings
from PIL import Image

try:
    from google import genai
except ImportError:
    pass

warnings.filterwarnings("ignore")

def analyze_videos():
    assets_dir = r"C:\Users\pc\Documents\Antigravity\Social Media Content Editor\opus_clone\Assets"
    video_files = glob.glob(os.path.join(assets_dir, "*.MOV")) + glob.glob(os.path.join(assets_dir, "*.mp4"))
    
    if not video_files:
        print("No videos found.")
        return

    api_key = os.environ.get("GEMINI_API_KEY", os.environ.get("GOOGLE_API_KEY", ""))
    if not api_key:
        print("No API key found. Cannot analyze.")
        return
        
    client = genai.Client(api_key=api_key)
    
    print("\n--- ENGLABS VIDEO ANALYSIS ---")
    print("Extracting frames and asking Gemini Vision to analyze each one...\n")
    
    for vid in video_files:
        cap = cv2.VideoCapture(vid)
        if not cap.isOpened():
            print(f"- {os.path.basename(vid)}: Could not open video file.")
            continue
            
        # Grab a frame from exactly halfway through the video
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if total_frames > 0:
            cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames // 2)
            
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            print(f"- {os.path.basename(vid)}: Could not extract frame.")
            continue
            
        temp_img = "temp_frame.jpg"
        cv2.imwrite(temp_img, frame)
        
        img = Image.open(temp_img)
        
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=["You are a manufacturing expert. Look at this frame from a video. Tell me exactly what process is happening here in ONE short sentence. Be descriptive about the action and materials.", img]
            )
            print(f"- {os.path.basename(vid)}: {response.text.strip()}")
        except Exception as e:
            print(f"- ERROR {os.path.basename(vid)}: Error analyzing frame ({e})")
            
        img.close()
        if os.path.exists(temp_img):
            os.remove(temp_img)

if __name__ == "__main__":
    analyze_videos()
