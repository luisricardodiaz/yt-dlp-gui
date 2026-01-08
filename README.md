# Simple yt-dlp GUI

A lightweight graphical interface for [yt-dlp](https://github.com/yt-dlp/yt-dlp) built with Python and Tkinter. This tool allows you to easily download videos and extract MP3 audio from YouTube and other supported sites.

## Features
- 🎥 Download videos (MP4)
- 🎵 Extract audio (MP3) with auto-conversion
- 📂 Select custom download folder
- 📊 Progress bar with real-time status

## Prerequisites
To use the MP3 conversion feature, you must have **FFmpeg** installed.
- **macOS:** `brew install ffmpeg`
- **Windows:** [Download FFmpeg](https://ffmpeg.org/download.html)

## Installation

1. **Clone the repository**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/yt-dlp-gui.git](https://github.com/YOUR_USERNAME/yt-dlp-gui.git)
   cd yt-dlp-gui

2. **Set up a Virtual Environment**
   # macOS / Linux
    python3 -m venv venv
    source venv/bin/activate

    # Windows
    python -m venv venv
    venv\Scripts\activate

3. **Install Dependencies**
    pip install -r requirements.txt


## Usage

Run the script using Python:

    python downloader_gui.py OR python3 downloader_gui.py


