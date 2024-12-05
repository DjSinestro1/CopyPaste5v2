import os
import shutil
import time
import sys
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

# Attempt to import psutil, install if not found
try:
    import psutil
except ImportError:
    print("psutil not found. Attempting to install...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'psutil'])
    import psutil

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileCopyHandler(FileSystemEventHandler):
    def __init__(self, source_dir, destination_dirs, wait_time=5, max_retries=3):
        self.source_dir = source_dir
        self.destination_dirs = destination_dirs
        self.wait_time = wait_time
        self.max_retries = max_retries

    def is_file_locked(self, filepath):
        """Check if file is in use by another process"""
        try:
            os.rename(filepath, filepath)
            return False
        except (OSError, PermissionError):
            return True

    def wait_for_file_ready(self, filepath):
        """Wait for file to be fully available"""
        for attempt in range(self.max_retries):
            try:
                time.sleep(self.wait_time)
                initial_size = os.path.getsize(filepath)
                time.sleep(1)
                final_size = os.path.getsize(filepath)
                if initial_size == final_size and not self.is_file_locked(filepath):
                    return True
            except Exception as e:
                print(f"File check attempt {attempt + 1} failed: {e}")
        
        return False

    def on_created(self, event):
        if not event.is_directory:
            source_path = event.src_path
            
            if not self.wait_for_file_ready(source_path):
                print(f"File {source_path} not ready after multiple attempts")
                return

            relative_path = os.path.relpath(source_path, self.source_dir)
            
            for dest_dir in self.destination_dirs:
                try:
                    full_dest_path = os.path.join(dest_dir, relative_path)
                    os.makedirs(os.path.dirname(full_dest_path), exist_ok=True)
                    shutil.copy2(source_path, full_dest_path)
                    print(f"Successfully copied {relative_path} to {full_dest_path}")
                
                except Exception as e:
                    print(f"Error copying {relative_path} to {dest_dir}: {e}")

def browse_directory(entry_widget):
    directory = filedialog.askdirectory()
    if directory:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, directory)

def start_monitoring():
    source_directory = entry_source_directory.get()
    destination_directories = [
        entry_target_directory_1.get(),
        entry_target_directory_2.get(),
        entry_target_directory_3.get(),
        entry_target_directory_4.get(),
        entry_target_directory_5.get()
    ]
    
    if not os.path.isdir(source_directory):
        messagebox.showerror("Error", "Please select a valid source directory.")
        return
    
    for target_directory in destination_directories:
        if not os.path.isdir(target_directory):
            messagebox.showerror("Error", f"Please select a valid target directory: {target_directory}.")
            return
    
    # Create the event handler with custom wait times
    event_handler = FileCopyHandler(
        source_dir=source_directory,
        destination_dirs=destination_directories,
        wait_time=5,
        max_retries=3
    )
    
    observer = Observer()
    observer.schedule(event_handler, source_directory, recursive=True)
    
    observer.start()
    
    try:
        print(f"Monitoring {source_directory} for new files...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()

# Create the main window
root = tk.Tk()
root.title("File Monitor and Copier")

# Source Directory selection
frame_source = tk.Frame(root)
frame_source.pack(padx=10, pady=5)

label_source_directory = tk.Label(frame_source, text="Select Source Directory:")
label_source_directory.grid(row=0, column=0, padx=5, pady=5)

entry_source_directory = tk.Entry(frame_source, width=50)
entry_source_directory.grid(row=0, column=1, padx=5, pady=5)

button_browse_source = tk.Button(frame_source, text="Browse", command=lambda: browse_directory(entry_source_directory))
button_browse_source.grid(row=0, column=2, padx=5, pady=5)

# Target Directory 1 selection
frame_target_1 = tk.Frame(root)
frame_target_1.pack(padx=10, pady=5)

label_target_directory_1 = tk.Label(frame_target_1, text="Select Target Directory 1:")
label_target_directory_1.grid(row=0, column=0, padx=5, pady=5)

entry_target_directory_1 = tk.Entry(frame_target_1, width=50)
entry_target_directory_1.grid(row=0, column=1, padx=5, pady=5)

button_browse_target_1 = tk.Button(frame_target_1, text="Browse", command=lambda: browse_directory(entry_target_directory_1))
button_browse_target_1.grid(row=0, column=2, padx=5, pady=5)

# Target Directory 2 selection
frame_target_2 = tk.Frame(root)
frame_target_2.pack(padx=10, pady=5)

label_target_directory_2 = tk.Label(frame_target_2, text="Select Target Directory 2:")
label_target_directory_2.grid(row=0, column=0, padx=5, pady=5)

entry_target_directory_2 = tk.Entry(frame_target_2, width=50)
entry_target_directory_2.grid(row=0, column=1, padx=5, pady=5)

button_browse_target_2 = tk.Button(frame_target_2, text="Browse", command=lambda: browse_directory(entry_target_directory_2))
button_browse_target_2.grid(row=0, column=2, padx=5, pady=5)

# Target Directory 3 selection
frame_target_3 = tk.Frame(root)
frame_target_3.pack(padx=10, pady=5)

label_target_directory_3 = tk.Label(frame_target_3, text="Select Target Directory 3:")
label_target_directory_3.grid(row=0, column=0, padx=5, pady=5)

entry_target_directory_3 = tk.Entry(frame_target_3, width=50)
entry_target_directory_3.grid(row=0, column=1, padx=5, pady=5)

button_browse_target_3 = tk.Button(frame_target_3, text="Browse", command=lambda: browse_directory(entry_target_directory_3))
button_browse_target_3.grid(row=0, column=2, padx=5, pady=5)

# Target Directory 4 selection
frame_target_4 = tk.Frame(root)
frame_target_4.pack(padx=10, pady=5)

label_target_directory_4 = tk.Label(frame_target_4, text="Select Target Directory 4:")
label_target_directory_4.grid(row=0, column=0, padx=5, pady=5)

entry_target_directory_4 = tk.Entry(frame_target_4, width=50)
entry_target_directory_4.grid(row=0, column=1, padx=5, pady=5)

button_browse_target_4 = tk.Button(frame_target_4, text="Browse", command=lambda: browse_directory(entry_target_directory_4))
button_browse_target_4.grid(row=0, column=2, padx=5, pady=5)

# Target Directory 5 selection
frame_target_5 = tk.Frame(root)
frame_target_5.pack(padx=10, pady=5)

label_target_directory_5 = tk.Label(frame_target_5, text="Select Target Directory 5:")
label_target_directory_5.grid(row=0, column=0, padx=5, pady=5)

entry_target_directory_5 = tk.Entry(frame_target_5, width=50)
entry_target_directory_5.grid(row=0, column=1, padx=5, pady=5)

button_browse_target_5 = tk.Button(frame_target_5, text="Browse", command=lambda: browse_directory(entry_target_directory_5))
button_browse_target_5.grid(row=0, column=2, padx=5, pady=5)

# Start monitoring button
button_start = tk.Button(root, text="Start Monitoring", command=start_monitoring)
button_start.pack(pady=20)

root.mainloop()
