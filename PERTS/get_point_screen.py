import os
import re
import sys

try:
    import pynput
except ModuleNotFoundError:
    os.system("python -m pip install pynput")
    import pynput

try:
    import pyautogui
except ModuleNotFoundError:
    os.system("python -m pip install pyautogui")
    import pyautogui

try:
    import cv2  # noqa: F401  -- enables confidence-based image matching in pyautogui
except ModuleNotFoundError:
    os.system("python -m pip install opencv-python")

from pynput.mouse import Button, Controller

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "output.POS")


def extract_photo_path(args):
    """Find a `...photo_path="..."` style argument, tolerating any prefix/typo."""
    for arg in args:
        match = re.match(r"^-{1,2}\S*photo_path=(.+)$", arg, re.IGNORECASE)
        if match:
            return match.group(1).strip().strip('"').strip("'")
    return None


def locate_on_screen(photo_path):
    if not os.path.isfile(photo_path):
        print(f"Error: photo not found: {photo_path}")
        sys.exit(1)

    try:
        location = pyautogui.locateCenterOnScreen(photo_path, confidence=0.8)
    except TypeError:
        # opencv isn't available, confidence isn't supported without it
        location = pyautogui.locateCenterOnScreen(photo_path)

    if location is None:
        print(f"Could not find '{photo_path}' on screen.")
        sys.exit(1)

    return int(location.x), int(location.y)


def cmd_get_point(args):
    photo_path = extract_photo_path(args)
    if not photo_path:
        print('Error: missing "...photo_path=" argument.')
        sys.exit(1)

    x, y = locate_on_screen(photo_path)

    with open(OUTPUT_FILE, "w") as f:
        f.write(f"{x},{y}")

    print(f"Found at ({x}, {y}). Written to {OUTPUT_FILE}")


def cmd_click(args):
    photo_path = extract_photo_path(args)
    if not photo_path:
        print('Error: missing "...photo_path=" argument.')
        sys.exit(1)

    x, y = locate_on_screen(photo_path)

    mouse = Controller()
    mouse.position = (x, y)
    mouse.click(Button.left, 1)

    print(f"Clicked at ({x}, {y})")


def main():
    args = sys.argv[1:]

    if not args:
        print("Usage:")
        print('  python get_point_screen.py --get -point -example_photo_path="C:\\path\\to\\photo.png"')
        print('  python get_point_screen.py -click -example_photo_path="C:\\path\\to\\photo.png"')
        sys.exit(1)

    if "-click" in args:
        cmd_click(args)
    elif "--get" in args and "-point" in args:
        cmd_get_point(args)
    else:
        print("Error: unrecognized command. Use `--get -point` or `-click`.")
        sys.exit(1)


if __name__ == "__main__":
    main()