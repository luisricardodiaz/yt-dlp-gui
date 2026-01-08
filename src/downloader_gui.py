import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk  # Import ttk for the Progress Bar
import yt_dlp
import threading
import os

def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_var.set(folder_selected)
        display_text = folder_selected
        if len(display_text) > 50:
            display_text = "..." + display_text[-45:]
        folder_label.config(text=f"Save to: {display_text}")

def progress_hook(d):
    """
    This function is called by yt-dlp repeatedly during the download.
    'd' is a dictionary containing status information.
    """
    if d['status'] == 'downloading':
        # 1. Get the percentage string (e.g., "45.5%")
        p_str = d.get('_percent_str', '0%').replace('%','')
        
        try:
            # 2. Convert to a float number
            progress_value = float(p_str)
            
            # 3. Update the Progress Bar and Label
            # We use root.after to update GUI from a background thread safely
            root.after(0, update_progress_ui, progress_value, f"Downloading: {d.get('_percent_str')}")
            
        except ValueError:
            pass

    elif d['status'] == 'finished':
        root.after(0, update_progress_ui, 100, "Processing / Converting...")

def update_progress_ui(value, message):
    """
    Helper to update GUI elements safely.
    """
    progress_bar['value'] = value
    status_label.config(text=f"Status: {message}")

def download_content():
    url = url_entry.get()
    save_path = folder_var.get()
    
    if not url:
        messagebox.showerror("Error", "Please enter a URL")
        return

    download_button.config(state=tk.DISABLED, text="Downloading...")
    status_label.config(text="Status: Starting...")
    progress_bar['value'] = 0  # Reset progress bar

    selected_format = format_var.get()

    thread = threading.Thread(target=run_yt_dlp, args=(url, selected_format, save_path))
    thread.start()

def run_yt_dlp(url, selected_format, save_path):
    ydl_opts = {
        'paths': {'home': save_path},
        'format': 'best',
        'outtmpl': '%(title)s.%(ext)s',
        'progress_hooks': [progress_hook], # Attach the hook here!
    }

    if selected_format == "Audio Only (MP3)":
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # Final success update
        root.after(0, lambda: status_label.config(text="Status: Download Complete!", fg="green"))
        
    except Exception as e:
        root.after(0, lambda: status_label.config(text="Status: Error occurred.", fg="red"))
        print(f"Error: {e}")
        
    finally:
        root.after(0, lambda: download_button.config(state=tk.NORMAL, text="Download"))

# --- GUI SETUP ---

root = tk.Tk()
root.title("My yt-dlp GUI")
root.geometry("500x500") # Made taller again for progress bar

# 1. Video URL
tk.Label(root, text="Video URL:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# 2. Format Selection
tk.Label(root, text="Select Format:").pack(pady=5)
format_var = tk.StringVar(root)
format_var.set("Video (MP4)") 
format_options = ["Video (MP4)", "Audio Only (MP3)"]
format_menu = tk.OptionMenu(root, format_var, *format_options)
format_menu.pack(pady=5)

# 3. Folder Selection
tk.Label(root, text="Destination Folder:").pack(pady=5)
current_directory = os.getcwd()
folder_var = tk.StringVar(root, value=current_directory)
folder_btn = tk.Button(root, text="Select Folder", command=select_folder)
folder_btn.pack(pady=2)
folder_label = tk.Label(root, text=f"Save to: {current_directory}", fg="gray", wraplength=400)
folder_label.pack(pady=5)

# 4. Download Button
download_button = tk.Button(root, text="Download", command=download_content, bg="lightblue", font=("Arial", 12, "bold"))
download_button.pack(pady=15)

# 5. NEW: Progress Bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=10)

# 6. Status Label
status_label = tk.Label(root, text="Status: Ready", fg="blue")
status_label.pack(pady=10)

root.mainloop()