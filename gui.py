import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk
from image_tools import ImageHandler

class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Watermarking App")
        self.handler = ImageHandler()
        self.base_tk_image = None
        self.watermark_image = None
        self.watermark_tk_image = None
        self.watermark_id = None
        self.watermark_pos = [50, 50]
        self.watermark_size = [100, 100]
        self.dragging = False
        self.resizing = False
        self.offset = (0, 0)

        self.canvas = tk.Canvas(root, width=600, height=600, bg="gray")
        self.canvas.pack()

        btn_frame = tk.Frame(root)
        btn_frame.pack()
        tk.Button(btn_frame, text="Load Image", command=self.load_image).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Add Image Watermark", command=self.add_image_watermark).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="AI BG Remover", command=self.remove_bg_ai).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Merge & Save", command=self.merge_and_save).pack(side=tk.LEFT)

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Motion>", self.on_motion)

    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if path:
            img = self.handler.load_base_image(path)
            self.base_tk_image = ImageTk.PhotoImage(img.resize((600, 600)))
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor="nw", image=self.base_tk_image)
            self.watermark_id = None

    def add_image_watermark(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if path and self.handler.base_image:
            self.handler.load_watermark_image(path)
            self.watermark_size = [100, 100]
            self.watermark_pos = [50, 50]
            self.update_watermark_image()
            self.draw_watermark()

    def remove_bg_ai(self):
        if not self.handler.watermark_image_orig:
            messagebox.showerror("Error", "It's required to load a watermakr image first!")
            return

        self.handler.remove_bg_ai()
        self.update_watermark_image()
        self.draw_watermark()
        messagebox.showinfo("Done", "Background removed with AI!")

    def update_watermark_image(self):
        if self.handler.watermark_image_orig:
            self.watermark_image = self.handler.resize_image(
                self.handler.watermark_image_orig, tuple(self.watermark_size)
            )
            self.watermark_tk_image = ImageTk.PhotoImage(self.watermark_image)

    def draw_watermark(self):
        if self.watermark_id:
            self.canvas.delete(self.watermark_id)
        self.watermark_id = self.canvas.create_image(
            self.watermark_pos[0], self.watermark_pos[1],
            anchor="nw", image=self.watermark_tk_image, tags="watermark"
        )
        # Draw resize handle
        if hasattr(self, 'resize_handle'):
            self.canvas.delete(self.resize_handle)
        x1, y1 = self.watermark_pos
        x2, y2 = x1 + self.watermark_size[0], y1 + self.watermark_size[1]
        self.resize_handle = self.canvas.create_rectangle(
            x2-4, y2-4, x2+4, y2+4, fill="red", tags="resize_handle"
        )

    def on_press(self, event):
        if not self.watermark_id:
            return
        x1, y1 = self.watermark_pos
        x2, y2 = x1 + self.watermark_size[0], y1 + self.watermark_size[1]
        if x2 - 10 < event.x < x2 + 10 and y2 - 10 < event.y < y2 + 10:
            self.resizing = True
        elif x1 < event.x < x2 and y1 < event.y < y2:
            self.dragging = True
            self.offset = (event.x - x1, event.y - y1)

    def on_drag(self, event):
        if self.resizing:
            new_width = max(10, event.x - self.watermark_pos[0])
            new_height = max(10, event.y - self.watermark_pos[1])
            self.watermark_size = [new_width, new_height]
            self.update_watermark_image()
            self.draw_watermark()
        elif self.dragging:
            new_x = event.x - self.offset[0]
            new_y = event.y - self.offset[1]
            self.watermark_pos = [new_x, new_y]
            self.draw_watermark()

    def on_release(self, event):
        self.dragging = False
        self.resizing = False

    def on_motion(self, event):
        if not self.watermark_id:
            return
        x1, y1 = self.watermark_pos
        x2, y2 = x1 + self.watermark_size[0], y1 + self.watermark_size[1]
        if x2 - 10 < event.x < x2 + 10 and y2 - 10 < event.y < y2 + 10:
            self.canvas.config(cursor="bottom_right_corner")
        elif x1 < event.x < x2 and y1 < event.y < y2:
            self.canvas.config(cursor="fleur")
        else:
            self.canvas.config(cursor="")

    def merge_and_save(self):
        if not self.handler.base_image or not self.watermark_image:
            messagebox.showerror("Error", "Load both images first!")
            return
        base_img = self.handler.base_image
        pos = (int(self.watermark_pos[0] * base_img.width / 600),
               int(self.watermark_pos[1] * base_img.height / 600))
        size = (int(self.watermark_size[0] * base_img.width / 600),
                int(self.watermark_size[1] * base_img.height / 600))
        wm_resized = self.handler.resize_image(self.handler.watermark_image_orig, size)
        merged = self.handler.merge_images(base_img, wm_resized, pos)
        save_path = filedialog.asksaveasfilename(defaultextension=".png")
        if save_path:
            merged.save(save_path)
            messagebox.showinfo("Saved", f"Image saved to {save_path}")