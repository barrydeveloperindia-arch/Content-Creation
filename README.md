# 🏭 OpusClone by Englabs: Handover Document & Architecture

This document serves as the official handover and system architecture guide for the **Englabs AI Video Repurposing Pipeline** (OpusClone). This pipeline transforms raw, horizontal manufacturing footage into viral, 9:16 vertical shorts with motion tracking, Hormozi-style captions, and SEO-optimized metadata.

## 📁 System Architecture

The pipeline is split into distinct, modular Python engines:

### 1. Ingestion & Pre-processing (`batch_processor.py`, `ingestion.py`)
- Scans the `Assets/` directory for raw `.MOV` or `.mp4` iPhone footage.
- Queues files for sequential processing to prevent memory overflow.

### 2. The Transcription Engine (`transcription.py`)
- **Core Technology:** OpenAI Whisper (Local CPU).
- **Function:** Extracts highly accurate, word-level timestamps (`start` and `end`) for every spoken word in the factory footage. Saves the output as a `.json` transcript.

### 3. The Virality Brain (`llm_engine.py`)
- **Core Technology:** Google Gemini 2.5 Flash.
- **Function:** Ingests the Whisper transcript and hunts for "Oddly Satisfying" manufacturing moments, material handling, or final product reveals. 
- Returns structured JSON containing the `start_time`, `end_time`, a viral `hook`, and a `virality_score` (1-100).

### 4. The Virtual Cameraman (`cv_cropper.py`)
- **Core Technology:** OpenCV Background Subtraction.
- **Function:** Unlike OpusClip which relies on Face Tracking, this engine uses mathematical motion tracking. It finds the largest moving object (like a spray gun or CNC arm) and dynamically pans the 9:16 vertical crop to keep the action perfectly centered.

### 5. The Caption Renderer (`caption_engine.py`)
- **Core Technology:** Pillow (PIL) + MoviePy.
- **Function:** Renders "Hormozi-style" captions. All text is uppercase, bold, and outlined with a heavy black stroke. Words longer than 5 letters are dynamically highlighted in Englabs Yellow (`#FFD700`) to maximize viewer retention.

### 6. The V4 Masterpiece Engine (`montage_engine.py`)
- **Core Technology:** MoviePy + Libx264.
- **Function:** Stitches the final output together.
  - Generates a **Loud Label** (Hook Text) for the first 3 seconds to stop the scroll.
  - Crossfades all clips using native FFmpeg at 20Mbps (`yuv420p` pixel format) to ensure flawless playback on Windows, TikTok, and Instagram.
  - Appends an Englabs Logo fade-to-black Outro.

### 7. The SEO Generator (`seo_generator.py`)
- **Core Technology:** Gemini.
- **Function:** Reads the visual context and generates YouTube/TikTok ready metadata (Titles, Descriptions, Hashtags).

### 8. The Human-In-The-Loop UI (`review_app.py`, `templates/`)
- **Core Technology:** Flask + HTML/CSS.
- **Function:** An exact visual replica of the OpusClip SaaS dashboard. Allows the marketing team to drop folders, review AI-selected hooks, tweak timestamps, and click "Save and Compile" before final rendering.

---

## 🚀 Master Task List (What's Left?)

While the V4 pipeline is now 100% operational and pushed to Git, the following modular skills can be added in Phase 2:

- [ ] **Instagram API Integration:** Build a script that takes `ENGLABS_WORKFLOW_MONTAGE_V4.mp4` and the `seo.json` and automatically pushes it to Instagram Reels via the Graph API.
- [ ] **YouTube API Integration:** Build a YouTube Shorts publisher script.
- [ ] **Background Worker:** Move the heavy MoviePy rendering off the Flask main thread into a `Celery` worker or a simple `queue` so the UI doesn't hang while rendering.
- [ ] **Dynamic Color Palettes:** Add a UI toggle to let the user switch between Englabs Yellow, Cyberpunk Neon, or Classic White for the caption highlights.
