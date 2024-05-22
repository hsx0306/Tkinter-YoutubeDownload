from tkinter import *
from tkinter import messagebox, ttk
from PIL import ImageTk, Image
from io import BytesIO
import yt_dlp
import threading
import requests

def fetch_thumbnail_and_title(event):
    url = url_entry.get()
    if url:
        try:
            info = yt.extract_info(url, download=False)
            display_thumbnail(info['thumbnail'])
            display_title(info['title'])
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def download_audio(url : str):
    try:
        yt = yt_dlp.YoutubeDL(ydl_opts)
        yt.download([url])
        messagebox.showinfo("Success", "Audio downloaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def display_thumbnail(thumbnail_url):
    try:
        response = requests.get(thumbnail_url)
        image_bytes = response.content
        thumbnail_image = Image.open(BytesIO(image_bytes))
        thumbnail_image.thumbnail((150, 150))
        thumbnail_render = ImageTk.PhotoImage(thumbnail_image)
        thumbnail_label.config(image=thumbnail_render)
        thumbnail_label.image = thumbnail_render
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def display_title(title):
    title_label.config(text=f"Title: {title}")

def update_progress_bar(d):
    if d['status'] == 'downloading':
        p = d['_percent_str'].strip().replace('%', '').replace('\x1b[0m', '').replace('\x1b[94m', '')
        try:
            p = float(p)
            progress_bar["value"] = p
        except ValueError:
            pass
    elif d['status'] == 'finished':
        progress_bar["value"] = 100

def on_download():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a URL.")
        return

    # Perform download in a separate thread
    threading.Thread(target=download_audio, args=(url,), daemon=True).start()

app = Tk()
app.title("YouTube Audio Downloader")

# Left Frame for Thumbnail and Title
left_frame = Frame(app)
left_frame.pack(side=LEFT, padx=10, pady=10)

label = Label(left_frame, text="Enter the URL of the video you want to download audio from:")
label.grid(row=0, column=0, columnspan=2, pady=5)

url_entry = Entry(left_frame, width=30)
url_entry.grid(row=1, column=0, padx=5, pady=5)
url_entry.bind('<FocusOut>', fetch_thumbnail_and_title)  # Bind the event

thumbnail_label = Label(left_frame)
thumbnail_label.grid(row=2, column=0, padx=5, pady=5)

title_label = Label(left_frame, wraplength=200, justify="center")
title_label.grid(row=3, column=0, padx=5, pady=5)

# Right Frame for Download Button and Progress Bar
right_frame = Frame(app)
right_frame.pack(side=RIGHT, padx=10, pady=10)

download_button = Button(right_frame, text="Download", width=15, command=on_download)
download_button.grid(row=0, column=0, padx=5, pady=5)

progress_bar = ttk.Progressbar(right_frame, orient="horizontal", length=200, mode="determinate")
progress_bar.grid(row=1, column=0, padx=5, pady=5)

# Options for yt_dlp
output_template = "%(title)s.%(ext)s"
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',
    }],
    'ffmpeg_location': 'ffmpeg/',
    'outtmpl': output_template,
    'progress_hooks': [update_progress_bar]
}

yt = yt_dlp.YoutubeDL()

app.mainloop()
