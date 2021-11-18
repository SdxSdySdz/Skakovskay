from PIL import Image, ImageTk

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
