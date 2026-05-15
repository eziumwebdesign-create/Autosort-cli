# AutoSort CLI

A command-line tool that automatically organizes files into categorized folders based on file type and modification date.

Built with Python

---

## Features

- Sorts files into folders by type (Images, Videos, Documents, Code, etc.)
- --dry-run mode to preview changes before moving anything
- --by-date flag to add YYYY-MM subfolders inside each category
- Handles filename conflicts automatically
- Custom config file support (~/.autosort_config.json)
- Supports 60+ file extensions out of the box

---

## Usage

python autosort.py ~/Downloads
python autosort.py ~/Downloads --dry-run
python autosort.py ~/Downloads --by-date
python autosort.py ~/Downloads --verbose
python autosort.py --show-config
python autosort.py --reset-config

---

## Default Categories

Images: .jpg .jpeg .png .gif .svg .webp
Videos: .mp4 .mov .avi .mkv .webm
Audio: .mp3 .wav .flac .aac .ogg
Documents: .pdf .doc .docx .txt .md
Spreadsheets: .xls .xlsx .csv .numbers
Code: .py .js .ts .html .css .java
Archives: .zip .tar .gz .rar .7z
Misc: anything else

---

## Requirements

- Python 3.7+
- No external dependencies

---

## Author

ezio Zaytoun
