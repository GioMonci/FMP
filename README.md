# FMP

FMP (Fix My Photographs) is a simple Python image converter. It reads any
supported input image (PNG, JPEG, WebP, SVG, BMP, GIF, TIFF) and converts it to
the output format of your choice.

## Project setup

### 1. Download the project

Clone the repository with Git:

```bash
git clone https://github.com/GioMonci/FMP.git
cd FMP
```

Alternatively, download the repository as a ZIP from GitHub, extract it, and
open a terminal in the extracted `FMP` folder.

### 2. Create a virtual environment

Python 3.10 or newer is required.

SVG conversion also requires the Cairo system library. On macOS, install it
with [Homebrew](https://brew.sh/):

```bash
brew install cairo libffi
```

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```bash
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

With the virtual environment active, run:

```bash
python -m pip install -r requirements.txt
```

## Run the application

Start the graphical interface:

```bash
python -m src.gui
```

Choose an image, pick an **Output format**, confirm or change the output path,
and select **Convert**. By default, converted images are saved in your
Downloads folder.

## Command-line usage

You can also convert an image directly from the terminal. Without a destination,
the image is saved to your Downloads folder as PNG:

```bash
python -m src.main input.webp
```

Choose the output format with a destination extension:

```bash
python -m src.main input.svg output.jpg
```

Or with the `--format` flag (png, jpg/jpeg, webp, bmp, gif, tiff/tif):

```bash
python -m src.main input.png --format webp
```
