import os
# Configure Numba cache settings before any imports
cache_dir = os.path.join(os.environ.get("TEMP", "/tmp"), "numba_cache")
os.makedirs(cache_dir, exist_ok=True)
os.environ["NUMBA_CACHE_DIR"] = cache_dir
os.environ["NUMBA_DISABLE_CACHE"] = "1"

import tkinter as tk
from gui import WatermarkApp

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    app = WatermarkApp(root)
    root.mainloop()