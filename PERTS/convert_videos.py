"""
Video/Audio Converter

Asks the user for a target file type (e.g. webm, mp4, mp3), then a folder.
Scans the folder (including subfolders) for media files that are NOT already
that type and converts them to the requested type using ffmpeg.

Requires ffmpeg to be installed and available on PATH.
Download: https://ffmpeg.org/download.html
"""

import os
import shutil
import subprocess
import sys

# Extensions considered "media" files that we should look at / possibly convert.
MEDIA_EXTENSIONS = {
    ".mp4", ".mkv", ".mov", ".avi", ".webm", ".flv", ".wmv", ".m4v",
    ".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a", ".wma",
}

# Formats that only carry audio - used to decide ffmpeg args (no video track needed).
AUDIO_ONLY_EXTENSIONS = {".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a", ".wma"}


def check_ffmpeg_available():
    if shutil.which("ffmpeg") is None:
        print("Error: ffmpeg was not found on your PATH.")
        print("Install it from https://ffmpeg.org/download.html and try again.")
        sys.exit(1)


def ask_target_extension():
    while True:
        answer = input("What file type do you want to convert to? (e.g. mp4, webm, mp3): ").strip().lower()
        answer = answer.lstrip(".")
        if not answer:
            print("Please enter a file type.")
            continue
        ext = "." + answer
        if ext not in MEDIA_EXTENSIONS:
            confirm = input(
                f"'{answer}' is not a recognized common media type. Use it anyway? (y/n): "
            ).strip().lower()
            if confirm != "y":
                continue
        return ext


def ask_folder():
    while True:
        folder = input("Enter the path to the folder to scan: ").strip().strip('"')
        if os.path.isdir(folder):
            return folder
        print(f"'{folder}' is not a valid folder. Try again.")


def find_files_to_convert(folder, target_ext):
    matches = []
    for root, _dirs, files in os.walk(folder):
        for name in files:
            ext = os.path.splitext(name)[1].lower()
            if ext in MEDIA_EXTENSIONS and ext != target_ext:
                matches.append(os.path.join(root, name))
    return matches


def convert_file(path, target_ext):
    base, _old_ext = os.path.splitext(path)
    output_path = base + target_ext

    # Avoid overwriting an existing file with the target name.
    if os.path.exists(output_path):
        print(f"Skipping (output already exists): {output_path}")
        return False

    cmd = ["ffmpeg", "-y", "-i", path]

    if target_ext in AUDIO_ONLY_EXTENSIONS:
        cmd += ["-vn"]

    cmd.append(output_path)

    print(f"Converting: {path} -> {output_path}")
    result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        print(f"Failed to convert {path}:\n{result.stderr.strip()[-500:]}")
        return False

    return True


def main():
    check_ffmpeg_available()

    target_ext = ask_target_extension()
    folder = ask_folder()

    files = find_files_to_convert(folder, target_ext)

    if not files:
        print(f"No files needing conversion to {target_ext} were found in '{folder}'.")
        return

    print(f"\nFound {len(files)} file(s) to convert to {target_ext}.\n")

    converted = 0
    failed = 0
    for path in files:
        if convert_file(path, target_ext):
            converted += 1
        else:
            failed += 1

    print(f"\nDone. Converted: {converted}, Failed/Skipped: {failed}")


if __name__ == "__main__":
    main()
