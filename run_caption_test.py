import os
from caption_engine import render_captions

def test():
    video = r"C:\Users\pc\Documents\Antigravity\Social Media Content Editor\opus_clone\temp_assets\IMG_9585_vertical.mp4"
    transcript = r"C:\Users\pc\Documents\Antigravity\Social Media Content Editor\opus_clone\temp_assets\IMG_9585_transcript.json"
    output = r"C:\Users\pc\Documents\Antigravity\Social Media Content Editor\opus_clone\temp_assets\IMG_9585_FINAL.mp4"
    
    render_captions(video, transcript, output)

if __name__ == "__main__":
    test()
