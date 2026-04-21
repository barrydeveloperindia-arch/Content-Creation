import cv2
import numpy as np
import os

def track_and_crop(video_path, output_path, target_ratio=(9, 16)):
    """
    Phase 4: Computer Vision Auto-Cropper
    Reads a horizontal video, tracks the primary motion, and automatically crops/pans 
    to a vertical 9:16 aspect ratio while keeping the action centered.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error opening video {video_path}")
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Calculate 9:16 crop dimensions
    target_width = int(height * (target_ratio[0] / target_ratio[1]))
    
    # Setup the video writer
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (target_width, height))

    # Initialize Background Subtractor for Motion Tracking
    # Why Motion Tracking? In manufacturing, the "action" is often a spray gun or a moving part, 
    # not necessarily a face, so FaceTracking might fail if they wear masks.
    back_sub = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=False)

    # Start the camera in the exact middle of the horizontal frame
    current_center_x = width // 2
    
    # Easing factor for smooth camera panning (0.0 means no movement, 1.0 means instant jerky movement)
    smoothing = 0.05 

    print(f"Cropping {os.path.basename(video_path)} to {target_ratio[0]}:{target_ratio[1]}...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # 1. Computer Vision Motion Tracking
        fg_mask = back_sub.apply(frame)
        
        # Morphological opening to clean up tiny dust/noise in the mask
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, np.ones((5,5), np.uint8))
        
        # Find all moving objects in the frame
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        target_x = current_center_x
        if contours:
            # Find the largest moving object (likely the worker or the tool)
            largest_contour = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest_contour) > 1500: # Filter out tiny noise
                x, y, w, h = cv2.boundingRect(largest_contour)
                target_x = x + (w // 2)

        # 2. Smooth Panning Algorithm (The "Virtual Cameraman")
        # Move the current center slightly towards the target motion to prevent jerky camera movements
        current_center_x += (target_x - current_center_x) * smoothing

        # 3. Calculate Bounding Box
        start_x = int(current_center_x - (target_width / 2))
        end_x = int(current_center_x + (target_width / 2))

        # Clamp the box to the edges to prevent black bars if the action goes too far left/right
        if start_x < 0:
            start_x = 0
            end_x = target_width
        elif end_x > width:
            end_x = width
            start_x = width - target_width

        # Crop the frame array
        cropped_frame = frame[:, start_x:end_x]
        
        # Write to the new vertical video file
        out.write(cropped_frame)

    cap.release()
    out.release()
    print(f"Saved cropped vertical video to {output_path}")
    return output_path

if __name__ == "__main__":
    print("Phase 4: Computer Vision Cropper Ready.")
    # Example usage:
    # input_vid = "Assets/IMG_9584.MOV"
    # output_vid = "temp_assets/IMG_9584_cropped.mp4"
    # track_and_crop(input_vid, output_vid)
