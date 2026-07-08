"""Image conversion logic and command-line interface for FMP."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from PIL import Image


def default_output_path(source: str | Path) -> Path:
    """Return the default PNG path in the user's Downloads folder."""
    source_path = Path(source).expanduser()
    return Path.home() / "Downloads" / f"{source_path.stem}.png"


def convert_to_png(source: str | Path, destination: str | Path | None = None) -> Path:
    """Convert a raster image or SVG file to PNG and return the output path."""
    source_path = Path(source).expanduser()
    if not source_path.is_file():
        raise FileNotFoundError(f"Input file not found: {source_path}")

    if destination:
        destination_path = Path(destination).expanduser()
    else:
        destination_path = default_output_path(source_path)
    destination_path = destination_path.with_suffix(".png")
    destination_path.parent.mkdir(parents=True, exist_ok=True)

    if source_path.suffix.lower() == ".svg":
        if sys.platform == "darwin":
            os.environ.setdefault(
                "DYLD_FALLBACK_LIBRARY_PATH",
                "/opt/homebrew/lib:/usr/local/lib",
            )

        try:
            import cairosvg
        except OSError as error:
            raise RuntimeError(
                "SVG conversion requires the Cairo system library. "
                "On macOS, install it with: brew install cairo libffi"
            ) from error

        cairosvg.svg2png(
            url=str(source_path),
            write_to=str(destination_path),
        )
    else:
        with Image.open(source_path) as image:
            image.save(destination_path, format="PNG")

    return destination_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert JPEG, WebP, SVG, and other supported images to PNG."
    )
    parser.add_argument("source", help="Path to the image to convert")
    parser.add_argument(
        "destination",
        nargs="?",
        help="Optional output path (defaults to the Downloads folder)",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    output_path = convert_to_png(args.source, args.destination)
    print(f"Converted image: {output_path}")


if __name__ == "__main__":
    main()
