#!/usr/bin/env python3
"""
AutoSort CLI - Automatically organize files into categorized folders
Usage: python autosort.py [directory] [options]
"""

import os
import sys
import shutil
import argparse
import json
from datetime import datetime
from pathlib import Path

DEFAULT_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico", ".tiff"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm", ".m4v"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".odt", ".rtf", ".md"],
    "Spreadsheets": [".xls", ".xlsx", ".csv", ".numbers"],
    "Presentations": [".ppt", ".pptx", ".key"],
    "Code": [".py", ".js", ".ts", ".html", ".css", ".java", ".c", ".cpp", ".go", ".rb", ".php", ".sh", ".json", ".xml", ".yaml", ".yml"],
    "Archives": [".zip", ".tar", ".gz", ".rar", ".7z", ".bz2"],
    "Executables": [".exe", ".dmg", ".pkg", ".deb", ".rpm", ".msi"],
    "Fonts": [".ttf", ".otf", ".woff", ".woff2"],
}

CONFIG_FILE = Path.home() / ".autosort_config.json"


def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return DEFAULT_CATEGORIES


def get_category(extension, categories):
    ext = extension.lower()
    for category, extensions in categories.items():
        if ext in extensions:
            return category
    return "Misc"


def get_dated_subfolder(filepath):
    mtime = os.path.getmtime(filepath)
    return datetime.fromtimestamp(mtime).strftime("%Y-%m")


def sort_directory(target_dir, dry_run=False, by_date=False, verbose=False, categories=None):
    target = Path(target_dir).resolve()

    if not target.exists():
        print(f"Error: Directory '{target}' does not exist.")
        sys.exit(1)

    if categories is None:
        categories = load_config()

    moved = 0
    skipped = 0
    errors = 0
    summary = {}

    print(f"\n{'[DRY RUN] ' if dry_run else ''}Sorting: {target}\n")

    for item in sorted(target.iterdir()):
        if item.name.startswith('.') or item.is_dir():
            continue
        if item.name == os.path.basename(__file__):
            continue

        ext = item.suffix
        category = get_category(ext, categories)

        dest_folder = target / category
        if by_date:
            dest_folder = dest_folder / get_dated_subfolder(item)

        dest_path = dest_folder / item.name

        if dest_path.exists():
            stem = item.stem
            suffix = item.suffix
            counter = 1
            while dest_path.exists():
                dest_path = dest_folder / f"{stem}_{counter}{suffix}"
                counter += 1

        action = f"  {item.name:40} → {category}{'/' + get_dated_subfolder(item) if by_date else ''}"

        if dry_run:
            print(action)
        else:
            try:
                dest_folder.mkdir(parents=True, exist_ok=True)
                shutil.move(str(item), str(dest_path))
                if verbose:
                    print(action)
                moved += 1
                summary[category] = summary.get(category, 0) + 1
            except Exception as e:
                print(f"  Error moving {item.name}: {e}")
                errors += 1
                skipped += 1

    if not dry_run:
        print(f"\nDone! Moved {moved} file(s).", end="")
        if skipped:
            print(f" Skipped {skipped} file(s) due to errors.", end="")
        print()
        if summary:
            print("\nSummary:")
            for cat, count in sorted(summary.items()):
                print(f"  {cat:20} {count} file(s)")
    else:
        print("\n[Dry run complete — no files were moved]")


def save_config(categories):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(categories, f, indent=2)
    print(f"Config saved to {CONFIG_FILE}")


def show_config():
    categories = load_config()
    print("\nCurrent category rules:\n")
    for category, extensions in categories.items():
        print(f"  {category:20} {', '.join(extensions)}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="AutoSort CLI — Automatically organize files into categorized folders",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python autosort.py ~/Downloads
  python autosort.py ~/Downloads --dry-run
  python autosort.py ~/Downloads --by-date --verbose
  python autosort.py --show-config
        """
    )

    parser.add_argument("directory", nargs="?", default=".", help="Directory to sort (default: current directory)")
    parser.add_argument("--dry-run", action="store_true", help="Preview what would happen without moving files")
    parser.add_argument("--by-date", action="store_true", help="Add YYYY-MM subfolders inside each category")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print every file action")
    parser.add_argument("--show-config", action="store_true", help="Show current category rules")
    parser.add_argument("--reset-config", action="store_true", help="Reset config to defaults")

    args = parser.parse_args()

    if args.show_config:
        show_config()
        return

    if args.reset_config:
        save_config(DEFAULT_CATEGORIES)
        print("Config reset to defaults.")
        return

    sort_directory(
        target_dir=args.directory,
        dry_run=args.dry_run,
        by_date=args.by_date,
        verbose=args.verbose
    )


if __name__ == "__main__":
    main()
