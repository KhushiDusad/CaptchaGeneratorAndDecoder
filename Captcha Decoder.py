import cv2
import numpy as np
import pytesseract
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'

class CaptchaDecoderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CAPTCHA Decoder")

        self.label = tk.Label(root, text="CAPTCHA Decoder", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.load_button = tk.Button(root, text="Load Image", command=self.load_image)
        self.load_button.pack()

        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()

        self.decode_button = tk.Button(root, text="Decode", command=self.decode_captcha)
        self.decode_button.pack()

        self.result_label = tk.Label(root, text="", font=("Helvetica", 12))
        self.result_label.pack(pady=10)

        self.image = None

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = Image.open(file_path)
            self.image.thumbnail((400, 400))
            self.photo = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
            self.result_label.config(text="")
    
    def decode_captcha(self):
        if self.image is not None:
            # Convert PIL image to OpenCV format
            cv_image = cv2.cvtColor(np.array(self.image), cv2.COLOR_RGB2BGR)
            # Apply preprocessing steps
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            closed = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, None)
            _, thresholded = cv2.threshold(closed, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            # Perform OCR
            captcha_text = pytesseract.image_to_string(thresholded)
            self.result_label.config(text="Captcha Text: " + captcha_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = CaptchaDecoderGUI(root)
    root.mainloop()
