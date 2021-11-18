from PIL import Image, ImageTk
import matplotlib.image as img
import numpy as np
import tkinter as tk


class ImageInfo:
    @property
    def PIL_image(self):
        return self._PIL_image
    
    @property
    def gray_image(self):
        return self._gray_image

    @property
    def binary_image(self):
        return self._binary_image

    @property
    def gray_image_as_string(self):
        return str(self._gray_image)
    
    @property
    def binary_image_as_string(self):
        return str(self._binary_image)

    @property
    def TK_gray_string_var(self):
        return self._TK_gray_string

    @property
    def TK_binary_string_var(self):
        return self._TK_binary_string
    
    @property
    def image_label(self):
        return self._image_label
    
    @property
    def gray_label(self):
        return self._gray_label

    @property
    def binary_label(self):
        return self._binary_label

    def __init__(self, app, image: Image, binary_threshold: float):
        self._PIL_image = image

        self._gray_image = (np.array(image) * 255).astype(int)[:, :, 0]
        self._binary_image = (self._gray_image >= (binary_threshold * 255)).astype(int)

        self._TK_gray_string = tk.StringVar()
        self._TK_binary_string = tk.StringVar()

        self._TK_gray_string.set(self.gray_image_as_string)
        self._TK_binary_string.set(self.binary_image_as_string)

        img = ImageTk.PhotoImage(Image.fromarray(self._gray_image))
        binary_img = ImageTk.PhotoImage(Image.fromarray(self._binary_image * 255))
        self._image_label = tk.Label(app, image=img)
        self._binary_image_label = tk.Label(app, image=binary_img)
        self._gray_label = tk.Label(app, textvariable=self._TK_gray_string)
        self._binary_label = tk.Label(app, textvariable=self._TK_binary_string)

        self._image_label.image = img
        self._binary_image_label.image = binary_img

    def init_image_label(self, row: int, column: int):
        self._image_label.grid(row=row, column=column)

    def init_gray_label(self, row: int, column: int):
        self._gray_label.grid(row=row, column=column)

    def init_binary_label(self, row: int, column: int):
        self._binary_label.grid(row=row, column=column)

    def init_binary_image_label(self, row: int, column: int):
        self._binary_image_label.grid(row=row, column=column)
