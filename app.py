from PIL import Image
from class_representative import ClassRepresentative
from representative_viewer import RepresentativeViewer

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

        delta = .5
        first_representative = ClassRepresentative(self, Image.open(first_img_path), delta)
        second_representative = ClassRepresentative(self, Image.open(second_img_path), delta)

        RepresentativeViewer.view(first_representative, column=0)
        RepresentativeViewer.view(second_representative, column=1)
