from PIL import Image
from image_info import ImageInfo

import tkinter as tk


first_img_path = "img/1.jpg"
second_img_path = "img/2.jpg"


class Application(tk.Frame):
    """Sample tkinter application class"""

    def __init__(self, master=None, title="<application>", **kwargs):
        """Create root window with frame, tune weight and resize"""
        super().__init__(master, **kwargs)
        self.master.title(title)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.grid(sticky="NEWS")
        self.create_widgets()
        for column in range(self.grid_size()[0]):
            self.columnconfigure(column, weight=1)
        for row in range(self.grid_size()[1]):
            self.rowconfigure(row, weight=1)

    def create_widgets(self):
        """Create all the widgets"""


class App(Application):
    def create_widgets(self):
        super().create_widgets()

        threshold = .5

        self._image_infos = (
            ImageInfo(self, Image.open(first_img_path), threshold),
            ImageInfo(self, Image.open(second_img_path), threshold),
        )

        self._img_size = (400, 400)

        for i in range(0, 2):
            img_info: ImageInfo = self._image_infos[i]
            img_info.show_gray_image(1, i)
            img_info.show_gray_matrix(2, i)
            img_info.show_binary_image(3, i)
            img_info.show_binary_matrix(4, i)
            img_info.show_standard_vector(5, i)
