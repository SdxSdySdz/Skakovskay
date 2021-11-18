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
        self._standard_vector = ArrayElement(app, self._binary_matrix.array.mean(axis=0))

    def show_gray_image(self, row: int, column: int):
        self.show_element(self._gray_image, row, column)

    def show_gray_matrix(self, row: int, column: int):
        self.show_element(self._gray_matrix, row, column)

    def show_binary_matrix(self, row: int, column: int):
        self.show_element(self._binary_matrix, row, column)

    def show_binary_image(self, row: int, column: int):
        self.show_element(self._binary_image, row, column)

    def show_standard_vector(self, row: int, column: int):
        self.show_element(self._standard_vector, row, column)

    def show_element(self, element: TK_Element, row: int, column: int):
        element.init_label(row, column)