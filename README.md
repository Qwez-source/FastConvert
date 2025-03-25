# FastConvert

FastConvert is a powerful and easy-to-use CLI tool for converting files between different formats.

## Features

- Convert images between formats (jpg, png, webp, gif, etc.)
- Convert videos between formats (mp4, avi, mkv, etc.)
- Convert videos to images (extracting first frame)

## Installation

```bash
pip install fastconvert
```

## Usage

Basic conversion:
```bash
fastconvert input_file output_file
```

Examples:
```bash
# Convert image from PNG to JPEG
fastconvert image.png image.jpg

# Convert video from MP4 to AVI
fastconvert video.mp4 video.avi

# Extract frame from video as image
fastconvert video.mp4 frame.jpg
```

## Supported Formats

See [FORMATS.md](FORMATS.md) for a complete list of supported formats and conversion capabilities.

## Requirements

- Python 3.6+
- See requirements.txt for Python dependencies

## License

MIT License
