from PIL import Image, ImageTk
import matplotlib.image as img
import numpy as np
import tkinter as tk


class TK_Element:
    @property
    def array(self):
        return self._array

    @property
    def array_as_string(self):
        return str(self._array)

    def __init__(self, app, array: np.ndarray):
        self._app = app
        self._array = array
        self._string_var: tk.StringVar = tk.StringVar()
        self._label: tk.Label = None

        self._string_var.set(self.array_as_string)

    def init_label(self, row: int, column: int):
        self.on_init_label()
        self._label.grid(row=row, column=column)

    def on_init_label(self):
        raise NotImplementedError()


class ArrayElement(TK_Element):
    def __init__(self, app, array: np.ndarray):
        super().__init__(app, array)

    def on_init_label(self):
        self._label = tk.Label(self._app, textvariable=self._string_var)


class ImageElement(TK_Element):
    def __init__(self, app, img_array: np.ndarray):
        super().__init__(app, img_array)

    def on_init_label(self):
        img = ImageTk.PhotoImage(Image.fromarray(self.array))
        self._label = tk.Label(self._app, image=img)
        self._label.image = img


class ImageInfo:
    def __init__(self, app, image: Image, binary_threshold: float):
        self._gray_image = ImageElement(app, np.array(image))
        self._gray_matrix = ArrayElement(app, (np.array(image) * 255).astype(int)[:, :, 0])
        self._binary_matrix = ArrayElement(app, (self._gray_matrix.array >= (binary_threshold * 255)).astype(int))
        self._binary_image = ImageElement(app, self._binary_matrix.array * 255)

    def init_image_label(self, row: int, column: int):
        self._gray_image.init_label(row, column)

    def init_gray_label(self, row: int, column: int):
        self._gray_matrix.init_label(row, column)

    def init_binary_label(self, row: int, column: int):
        self._binary_matrix.init_label(row, column)

    def init_binary_image_label(self, row: int, column: int):
        self._binary_image.init_label(row, column)
