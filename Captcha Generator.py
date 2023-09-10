import os
import random
import string
import tkinter as tk
from captcha.image import ImageCaptcha
from PIL import Image, ImageTk

class CaptchaGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CAPTCHA Generator")

        self.label = tk.Label(root, text="CAPTCHA Generator", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.custom_text_entry = tk.Entry(root, width=30)
        self.custom_text_entry.pack(pady=5)

        self.generate_button = tk.Button(root, text="Generate CAPTCHA", command=self.generate_captcha)
        self.generate_button.pack()

        self.canvas = tk.Canvas(root, width=280, height=90)
        self.canvas.pack()

    def generate_captcha(self):
        custom_text = self.custom_text_entry.get().strip()
        if not custom_text:
            captcha_length = 5
            custom_text = self.generate_random_string(captcha_length)
        
        image = ImageCaptcha(width=280, height=90)
        data = image.generate(custom_text)
        
        if not os.path.exists("captchas"):
            os.makedirs("captchas")

        image_path = os.path.join("captchas", f"{custom_text}.png")
        image.write(custom_text, image_path)

        captcha_image = Image.open(image_path)
        captcha_image.thumbnail((280, 90))
        self.photo = ImageTk.PhotoImage(captcha_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

    def generate_random_string(self, length):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

if __name__ == "__main__":
    root = tk.Tk()
    app = CaptchaGeneratorGUI(root)
    root.mainloop()
