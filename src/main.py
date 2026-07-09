"""Image conversion logic and command-line interface for FMP."""

from __future__ import annotations

import argparse
import io
import os
import sys
from pathlib import Path

from PIL import Image

# Maps a file extension (without the dot) to the Pillow format name used to
# save it. Several extensions can point at the same format (jpg/jpeg).
OUTPUT_FORMATS: dict[str, str] = {
    "png": "PNG",
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "webp": "WEBP",
    "bmp": "BMP",
    "gif": "GIF",
    "tiff": "TIFF",
    "tif": "TIFF",
}

# The default extension to use when saving each Pillow format.
DEFAULT_EXTENSION: dict[str, str] = {
    "PNG": "png",
    "JPEG": "jpg",
    "WEBP": "webp",
    "BMP": "bmp",
    "GIF": "gif",
    "TIFF": "tiff",
}


def resolve_format(value: str) -> str:
    """Return the Pillow format name for an extension or format string."""
    key = value.lower().lstrip(".")
    try:
        return OUTPUT_FORMATS[key]
    except KeyError:
        supported = ", ".join(sorted(DEFAULT_EXTENSION))
        raise ValueError(
            f"Unsupported output format: {value}. Supported formats: {supported}"
        ) from None


def default_output_path(source: str | Path, output_format: str = "png") -> Path:
    """Return the default output path in the user's Downloads folder."""
    source_path = Path(source).expanduser()
    extension = DEFAULT_EXTENSION[resolve_format(output_format)]
    return Path.home() / "Downloads" / f"{source_path.stem}.{extension}"


def _load_image(source_path: Path) -> Image.Image:
    """Open a raster image or render an SVG file into a Pillow image."""
    if source_path.suffix.lower() == ".svg":
        if sys.platform == "darwin":
            os.environ.setdefault(
                "DYLD_FALLBACK_LIBRARY_PATH",
                "/opt/homebrew/lib:/usr/local/lib",
            )

        try:
            import cairosvg
        except (OSError, ImportError) as error:
            raise RuntimeError(
                "SVG conversion requires the Cairo system library. "
                "On macOS, install it with: brew install cairo libffi"
            ) from error

        png_bytes = cairosvg.svg2png(url=str(source_path))
        return Image.open(io.BytesIO(png_bytes))

    return Image.open(source_path)


def _prepare_for_format(image: Image.Image, pillow_format: str) -> Image.Image:
    """Adjust the image mode so it can be saved in the target format."""
    if pillow_format == "JPEG" and image.mode not in ("RGB", "L"):
        # JPEG has no alpha channel, so flatten transparency onto white.
        rgba = image.convert("RGBA")
        background = Image.new("RGB", rgba.size, (255, 255, 255))
        background.paste(rgba, mask=rgba.split()[-1])
        return background
    return image


def convert_image(
    source: str | Path,
    destination: str | Path | None = None,
    output_format: str | None = None,
) -> Path:
    """Convert an image to the requested format and return the output path.

    The target format is chosen from ``output_format`` when given, otherwise
    from the ``destination`` extension, and defaults to PNG.
    """
    source_path = Path(source).expanduser()
    if not source_path.is_file():
        raise FileNotFoundError(f"Input file not found: {source_path}")

    if output_format:
        pillow_format = resolve_format(output_format)
    elif destination and Path(destination).suffix:
        pillow_format = resolve_format(Path(destination).suffix)
    else:
        pillow_format = "PNG"

    extension = DEFAULT_EXTENSION[pillow_format]

    if destination:
        destination_path = Path(destination).expanduser()
        if output_format or not destination_path.suffix:
            destination_path = destination_path.with_suffix(f".{extension}")
    else:
        destination_path = default_output_path(source_path, pillow_format)

    if destination_path == source_path:
        raise ValueError("Input and output paths must be different")
    destination_path.parent.mkdir(parents=True, exist_ok=True)

    with _load_image(source_path) as image:
        image = _prepare_for_format(image, pillow_format)
        image.save(destination_path, format=pillow_format)

    return destination_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert between image formats (PNG, JPEG, WebP, BMP, GIF, TIFF)."
    )
    parser.add_argument("source", help="Path to the image to convert")
    parser.add_argument(
        "destination",
        nargs="?",
        help="Optional output path (defaults to the Downloads folder)",
    )
    parser.add_argument(
        "-f",
        "--format",
        dest="output_format",
        choices=sorted(OUTPUT_FORMATS),
        help="Output format (defaults to png, or the destination extension)",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    output_path = convert_image(args.source, args.destination, args.output_format)
    print(f"Converted image: {output_path}")


if __name__ == "__main__":
    main()
