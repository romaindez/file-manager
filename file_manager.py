#!/usr/bin/env python3
"""
File Manager

This script automatically organizes files in a specified directory by moving them into
category-based subdirectories according to their file extensions.

Usage:
    1. Set the WATCH_DIRECTORY variable to the directory you want to monitor
    2. Run the script: python file_manager.py
    3. Files added to the watched directory will be automatically sorted into categories

The script creates category folders based on file extensions and moves files accordingly.
"""

import os
import sys
import time
import shutil
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# File extension mappings
EXTENSION_MAPPINGS = {
    "PDF": [".pdf"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"],
    "Video": [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm", ".m4v"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma"],
    "Documents": [
        ".doc",
        ".docx",
        ".xls",
        ".xlsx",
        ".ppt",
        ".pptx",
        ".txt",
        ".rtf",
        ".csv",
        ".odt",
    ],
    "Zip": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
    "Ebook": [".epub", ".mobi", ".azw", ".azw3", ".pdf"],
    "Installers": [".exe", ".dmg", ".pkg", ".app", ".msi"],
}

# Set the directory to watch (default is Downloads, but can be changed)
WATCH_DIRECTORY = os.path.expanduser("~/Downloads")


def get_category(file_extension):
    """Determine the category of a file based on its extension."""
    file_extension = file_extension.lower()
    for category, extensions in EXTENSION_MAPPINGS.items():
        if file_extension in extensions:
            return category
    return "Others"


def ensure_directory_exists(directory):
    """Create directory if it doesn't exist."""
    try:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            os.chmod(directory, 0o755)
    except Exception:
        raise


def get_unique_filename(destination_path):
    """Generate a unique filename if a file with the same name exists."""
    if not os.path.exists(destination_path):
        return destination_path

    base_path, extension = os.path.splitext(destination_path)
    counter = 1

    while True:
        new_path = f"{base_path}_{counter}{extension}"
        if not os.path.exists(new_path):
            return new_path
        counter += 1


class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            print(f"Directory created: {event.src_path} - ignoring")
            return

        try:
            # Wait a bit to ensure the file is completely written
            time.sleep(1)

            src_path = event.src_path
            print(f"File detected: {src_path}")

            if not os.path.exists(src_path):  # File might have been moved already
                print(f"File no longer exists: {src_path}")
                return

            # Ignore hidden files
            filename = os.path.basename(src_path)
            if filename.startswith("."):
                print(f"Skipping hidden file: {filename}")
                return

            # Get file extension and category
            _, extension = os.path.splitext(filename)
            if not extension:
                print(f"Skipping file without extension: {filename}")
                return

            category = get_category(extension)
            print(f"Categorized {filename} as {category}")

            # Create category directory if it doesn't exist
            category_path = os.path.join(WATCH_DIRECTORY, category)
            ensure_directory_exists(category_path)
            print(f"Ensuring category directory exists: {category_path}")

            # Generate destination path
            dest_path = os.path.join(category_path, filename)
            dest_path = get_unique_filename(dest_path)
            print(f"Destination path: {dest_path}")

            # Move the file
            shutil.move(src_path, dest_path)
            print(f"Moved file from {src_path} to {dest_path}")

            # Set file permissions to 644
            os.chmod(dest_path, 0o644)
            print(f"Set permissions on {dest_path}")

        except Exception as e:
            print(f"Error processing {event.src_path}: {str(e)}")
            import traceback

            print(traceback.format_exc())


def main():
    print(f"Starting file manager. Watching: {WATCH_DIRECTORY}")

    # Ensure all category directories exist
    for category in list(EXTENSION_MAPPINGS.keys()) + ["Others"]:
        try:
            category_path = os.path.join(WATCH_DIRECTORY, category)
            ensure_directory_exists(category_path)
            print(f"Created/verified category directory: {category_path}")
        except Exception as e:
            print(f"Failed to create directory for {category}: {str(e)}")
            sys.exit(1)

    # Initialize the observer
    try:
        observer = Observer()
        observer.schedule(FileHandler(), WATCH_DIRECTORY, recursive=False)
        print(f"Observer scheduled for: {WATCH_DIRECTORY}")
        observer.start()
        print("Observer started successfully")

        # Print process info for debugging
        pid = os.getpid()
        print(f"Process running with PID: {pid}")

        while True:
            time.sleep(1)
    except Exception as e:
        print(f"Error in main loop: {str(e)}")
        import traceback

        print(traceback.format_exc())
    except KeyboardInterrupt:
        print("Keyboard interrupt received. Stopping observer.")
        observer.stop()

    observer.join()
    print("File manager stopped")


if __name__ == "__main__":
    # Allow command-line specification of the watch directory
    if len(sys.argv) > 1:
        WATCH_DIRECTORY = os.path.abspath(sys.argv[1])
        print(f"Using specified watch directory: {WATCH_DIRECTORY}")

    main()
