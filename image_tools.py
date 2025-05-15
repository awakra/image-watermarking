from PIL import Image
from rembg import remove

class ImageHandler:
    def __init__(self):
        self.base_image = None
        self.watermark_image_orig = None

    def load_base_image(self, path):
        self.base_image = Image.open(path).convert("RGBA")
        return self.base_image

    def load_watermark_image(self, path):
        self.watermark_image_orig = Image.open(path).convert("RGBA")
        return self.watermark_image_orig

    def remove_bg_ai(self):
        if not self.watermark_image_orig:
            return
        img = self.watermark_image_orig.convert("RGBA")
        img_no_bg = remove(img)
        self.watermark_image_orig = img_no_bg

    def resize_image(self, img, size):
        return img.resize(size, Image.Resampling.LANCZOS)

    def merge_images(self, base_img, watermark_img, pos):
        merged = base_img.copy()
        merged.paste(watermark_img, pos, watermark_img)
        return merged