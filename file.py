import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import json
import os


class ImageEngine:
    def __init__(self):
        self.image = None

    def open(self, path):
        self.image = Image.open(path)
        return self.image

    def rotate(self):
        if self.image:
            self.image = self.image.rotate(90, expand=True)
        return self.image

    def resize(self, w, h):
        if self.image:
            self.image = self.image.resize((w, h))
        return self.image

    def brightness(self, v):
        if self.image:
            self.image = ImageEnhance.Brightness(self.image).enhance(v)
        return self.image

    def contrast(self, v):
        if self.image:
            self.image = ImageEnhance.Contrast(self.image).enhance(v)
        return self.image

    def blur(self):
        if self.image:
            self.image = self.image.filter(ImageFilter.BLUR)
        return self.image

    def save(self, path):
        if self.image:
            self.image.save(path)


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Photo Viewer PRO")
        self.root.geometry("1000x700")
        self.root.configure(bg="#0f1115")

        self.root.option_add("*Button.relief", "flat")
        self.root.option_add("*Button.highlightThickness", 0)

        self.engine = ImageEngine()

        self.image_label = tk.Label(
            root,
            bg="#0f1115",
            fg="#777777",
            text="Drag & Drop image here",
            font=("Arial", 18)
        )
        self.image_label.pack(expand=True, fill="both")

        self.panel = tk.Frame(root, bg="#151a22")
        self.panel.pack(fill="x")

        self.make_button("OPEN", self.open_file)
        self.make_button("ROTATE", self.rotate)
        self.make_button("RESIZE", self.resize)
        self.make_button("BRIGHT+", lambda: self.brightness(1.4))
        self.make_button("BRIGHT-", lambda: self.brightness(0.6))
        self.make_button("CONTRAST", lambda: self.contrast(1.5))
        self.make_button("BLUR", self.blur)
        self.make_button("SAVE", self.save)

        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind("<<Drop>>", self.drop)

        self.load_last()

    def make_button(self, text, cmd):
        btn = tk.Button(
            self.panel,
            text=text,
            command=cmd,
            bg="#2b2f3a",
            fg="#d0d0d0",
            activebackground="#3b4150",
            activeforeground="#ffffff",
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            font=("Arial", 10, "bold"),
            padx=14,
            pady=7,
            cursor="hand2"
        )
        btn.pack(side="left", padx=6, pady=8)

    def show(self, img):
        if img:
            img.thumbnail((950, 600))
            self.tk_img = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.tk_img, text="")

    def load_image(self, path):
        try:
            img = self.engine.open(path)
            self.show(img)
            self.save_last(path)
        except:
            messagebox.showerror("Error", "Cannot open image")

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg")])
        if path:
            self.load_image(path)

    def drop(self, event):
        path = event.data.strip()

        if path.startswith("{"):
            path = path.replace("{", "").replace("}", "")

        if os.path.isfile(path):
            self.load_image(path)

    def rotate(self):
        self.show(self.engine.rotate())

    def resize(self):
        try:
            w = int(simpledialog.askstring("Resize", "Width:"))
            h = int(simpledialog.askstring("Resize", "Height:"))
            self.show(self.engine.resize(w, h))
        except:
            messagebox.showerror("Error", "Invalid size")

    def brightness(self, v):
        self.show(self.engine.brightness(v))

    def contrast(self, v):
        self.show(self.engine.contrast(v))

    def blur(self):
        self.show(self.engine.blur())

    def save(self):
        path = filedialog.asksaveasfilename(defaultextension=".png")
        if path:
            self.engine.save(path)

    def save_last(self, path):
        try:
            with open("config.json", "w") as f:
                json.dump({"last": path}, f)
        except:
            pass

    def load_last(self):
        if os.path.exists("config.json"):
            try:
                with open("config.json") as f:
                    data = json.load(f)
                if "last" in data:
                    self.load_image(data["last"])
            except:
                pass


root = TkinterDnD.Tk()
app = App(root)
root.mainloop()
