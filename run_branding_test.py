import os
from branding import apply_watermark

def test():
    video = r"C:\Users\pc\Documents\Antigravity\Social Media Content Editor\opus_clone\temp_assets\IMG_9585_FINAL.mp4"
    logo = r"C:\Users\pc\OneDrive - Englabs India Pvt Ltd\Automate_trial_MANUFACTURE\Desktop\OLD DATA\ENGLABS-KARTIK\ENGLABS logo.png"
    
    # This will be the absolute final output ready for posting
    output = r"C:\Users\pc\Documents\Antigravity\Social Media Content Editor\opus_clone\READY_TO_POST_IMG_9585.mp4"
    
    apply_watermark(video, logo, output)

if __name__ == "__main__":
    test()
