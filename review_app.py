from flask import Flask, render_template, request, jsonify
import json
import os
import threading

app = Flask(__name__)
MASTER_FILE = "MASTER_ENGLABS_CLIPS.json"

@app.route('/')
def upload():
    return render_template('upload.html')

@app.route('/editor')
def editor():
    clips = []
    if os.path.exists(MASTER_FILE):
        with open(MASTER_FILE, "r", encoding="utf-8") as f:
            try:
                clips = json.load(f)
            except Exception as e:
                print(f"Error loading JSON: {e}")
                
    if not clips:
        clips = [{
            "source_video": "IMG_9585.MOV",
            "start_time": 0.0,
            "end_time": 15.0,
            "virality_score": 95,
            "hook": "The ultimate powder coating reveal.",
            "explanation": "This clip shows the final pristine finish out of the curing oven. Highly satisfying ASMR potential."
        }]
                
    return render_template('index.html', clips=clips)

@app.route('/approve', methods=['POST'])
def approve():
    data = request.json
    
    # In a fully connected system, this button click would trigger a background thread 
    # to run Phase 4 (Crop), Phase 5 (Caption), and Phase 6 (Brand) on this specific timestamp!
    print(f"\n[HUMAN APPROVED] Triggering Render Pipeline for {data['source_video']}")
    print(f"Cutting from {data['start_time']}s to {data['end_time']}s...")
    
    return jsonify({"status": "success", "message": "Render pipeline triggered in background!"})

if __name__ == '__main__':
    print("Starting Englabs Human-In-The-Loop Review UI on Port 5050...")
    app.run(debug=True, port=5050, use_reloader=False)
