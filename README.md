# Video Converter & Screen Point Tool

A small collection of local Windows utilities by thompog:

- **convert_videos.py** - Ask for a target file type (e.g. mp4, webm, mp3) and a folder, then
  scans that folder for media files that aren't already that type and converts them with
  ffmpeg. Requires ffmpeg on PATH.
- **get_point_screen.py** - Finds a UI element on screen from a screenshot/photo of it and
  either writes its (X, Y) coordinates to `output.POS`, or clicks it with the left mouse
  button.

## Usage

```
program --convert
program --get_point_screen --get -point -example_photo_path="C:\path\to\photo.png"
program --get_point_screen -click -example_photo_path="C:\path\to\photo.png"
```

## First run

On first launch you'll be shown the License, Terms of Service, and this README, and asked to
accept the Terms of Service before continuing.

## License

MIT License, see [LICENSE](LICENSE).

