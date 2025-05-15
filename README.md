# Image Watermarking App

A powerful and intuitive desktop application for adding watermarks to your images with ease. Built with Python and Tkinter, this app allows you to customize watermarks with drag-and-drop functionality and AI-powered background removal.

## Features

- **Image Loading**: Import base images in various formats (PNG, JPG, JPEG, BMP)
- **Watermark Customization**: Add image watermarks with full control over position and size
- **Interactive Interface**: Drag to position and resize watermarks intuitively
- **AI Background Removal**: One-click background removal for watermark images using advanced AI
- **High-Quality Output**: Preserve image quality while adding watermarks
- **Easy Export**: Save your watermarked images in PNG format

## Installation

Clone this repository:

```bash
git clone https://github.com/awakra/image-watermarking.git
cd image-watermarking
```

Create and activate a virtual environment:

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the application:

```bash
python main.py
```

1. Load your base image using the **"Load Image"** button
2. Add a watermark image using the **"Add Image Watermark"** button
3. Optionally remove the background from your watermark with the **"Remover Fundo IA"** button
4. Position and resize the watermark by dragging:
   - Drag the watermark to position it
   - Drag the red square in the bottom-right corner to resize
5. Save your watermarked image using the **"Merge & Save"** button

## Requirements

Dependencies listed in `requirements.txt`

## Technical Details

The application uses:

- **Tkinter**: For the graphical user interface
- **PIL/Pillow**: For image processing
- **rembg**: For AI-powered background removal
- **NumPy/Numba**: For efficient image operations

## Acknowledgments

- [rembg](https://github.com/danielgatis/rembg) for the amazing background removal technology
