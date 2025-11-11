import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import threading

# Convert function using ffmpeg
def convert_to_gif_ffmpeg(input_path, output_path, start=0, duration=None, scale=480, fps=15):
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    cmd = [
        "ffmpeg",
        "-ss", str(start),
        "-i", input_path
    ]

    if duration:
        cmd += ["-t", str(duration)]

    cmd += [
        "-vf", f"fps={fps},scale={scale}:-1:flags=lanczos",
        "-loop", "0",
        output_path
    ]

    subprocess.run(cmd, check=True)
    print(f"✅ GIF saved at: {output_path}")

# GUI logic
def select_input():
    path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
    if path:
        entry_input.delete(0, tk.END)
        entry_input.insert(0, path)

def select_output():
    path = filedialog.asksaveasfilename(defaultextension=".gif", filetypes=[("GIF files", "*.gif")])
    if path:
        entry_output.delete(0, tk.END)
        entry_output.insert(0, path)

def start_conversion():
    input_path = entry_input.get()
    output_path = entry_output.get()
    start = entry_start.get()
    duration = entry_duration.get()
    scale = entry_scale.get()
    fps = entry_fps.get()

    if not input_path or not os.path.exists(input_path):
        messagebox.showerror("Error", "Please select a valid MP4 file.")
        return

    if not output_path:
        base, _ = os.path.splitext(input_path)
        output_path = base + ".gif"

    start = float(start) if start else 0
    duration = float(duration) if duration else None
    scale = int(scale) if scale else 480
    fps = int(fps) if fps else 15

    def run_conversion():
        try:
            convert_to_gif_ffmpeg(input_path, output_path, start, duration, scale, fps)
            messagebox.showinfo("Success", f"GIF saved at:\n{output_path}")
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "FFmpeg execution failed. Please check your ffmpeg installation.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    threading.Thread(target=run_conversion).start()

# GUI layout
root = tk.Tk()
root.title("🎬 MP4 to GIF Converter (FFmpeg)")
root.geometry("520x360")
root.resizable(False, False)

tk.Label(root, text="Input MP4 File:").pack(anchor="w", padx=10, pady=(10, 0))
frame_input = tk.Frame(root)
frame_input.pack(fill="x", padx=10)
entry_input = tk.Entry(frame_input)
entry_input.pack(side="left", fill="x", expand=True)
tk.Button(frame_input, text="Browse", command=select_input).pack(side="right")

tk.Label(root, text="Output GIF File:").pack(anchor="w", padx=10, pady=(10, 0))
frame_output = tk.Frame(root)
frame_output.pack(fill="x", padx=10)
entry_output = tk.Entry(frame_output)
entry_output.pack(side="left", fill="x", expand=True)
tk.Button(frame_output, text="Save As", command=select_output).pack(side="right")

frame_opts = tk.Frame(root)
frame_opts.pack(padx=10, pady=10, fill="x")

tk.Label(frame_opts, text="Start (sec):").grid(row=0, column=0)
entry_start = tk.Entry(frame_opts, width=10)
entry_start.grid(row=0, column=1, padx=5)

tk.Label(frame_opts, text="Duration (sec):").grid(row=0, column=2)
entry_duration = tk.Entry(frame_opts, width=10)
entry_duration.grid(row=0, column=3, padx=5)

tk.Label(frame_opts, text="Scale width (px):").grid(row=1, column=0)
entry_scale = tk.Entry(frame_opts, width=10)
entry_scale.insert(0, "480")
entry_scale.grid(row=1, column=1, padx=5)

tk.Label(frame_opts, text="FPS:").grid(row=1, column=2)
entry_fps = tk.Entry(frame_opts, width=10)
entry_fps.insert(0, "15")
entry_fps.grid(row=1, column=3, padx=5)

tk.Button(root, text="🎞 Convert", command=start_conversion, bg="#4CAF50", fg="white",
          font=("Segoe UI", 12, "bold")).pack(pady=15, ipadx=10, ipady=5)

root.mainloop()
