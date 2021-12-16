import numpy as np
from PIL import Image
from class_representative import ClassRepresentative
from representative_viewer import RepresentativeViewer

import tkinter as tk
import matplotlib.pyplot as plt
import seaborn as sb

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

        delta = 39
        first_representative = ClassRepresentative(self, Image.open(first_img_path), delta)
        second_representative = ClassRepresentative(self, Image.open(second_img_path), delta)

        first_representative.solve_distances_matrix(second_representative)
        second_representative.solve_distances_matrix(first_representative)

        first_representative.solve_characteristics(second_representative, "first_representative_output")
        second_representative.solve_characteristics(first_representative, "second_representative_output")

        plt.plot(range(0, len(first_representative.kfes)), first_representative.kfes)
        plt.plot(range(0, len(second_representative.kfes)), second_representative.kfes)
        plt.show()

        # optimal_kfe, optimal_delta = 0, 0
        # for delta in range(0, 256):
        #     first_representative = ClassRepresentative(self, Image.open(first_img_path), delta)
        #     second_representative = ClassRepresentative(self, Image.open(second_img_path), delta)
        #
        #     first_representative.solve_distances_matrix(second_representative)
        #     second_representative.solve_distances_matrix(first_representative)
        #
        #     first_representative.solve_characteristics(second_representative, "first_representative_output")
        #     second_representative.solve_characteristics(first_representative, "second_representative_output")
        #
        #     kfe = np.max(first_representative.kfes)
        #
        #     if kfe > optimal_kfe:
        #         optimal_kfe = kfe
        #         optimal_delta = delta
        #
        # print(optimal_kfe, optimal_delta)
