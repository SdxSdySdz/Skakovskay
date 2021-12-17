import numpy as np
import pandas as pd
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

        delta = 45

        f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
        ax1.set_xlabel(f'distances (current delta {delta})')
        ax1.set_ylabel('kfe')

        ax2.set_xlabel('delta')


        first_representative = ClassRepresentative(self, Image.open(first_img_path), delta)
        second_representative = ClassRepresentative(self, Image.open(second_img_path), delta)

        first_representative.solve_distances_matrix(second_representative)
        second_representative.solve_distances_matrix(first_representative)

        first_representative.solve_characteristics(second_representative, "before")
        second_representative.solve_characteristics(first_representative, "second_representative_output")

        ax1.plot(range(0, len(first_representative.kfes)), first_representative.kfes)
        # ax1.plot(range(0, len(second_representative.kfes)), second_representative.kfes)

        kfes = []
        optimal_kfe, optimal_delta = 0, 0
        delta_range = list(range(20, 100))
        for delta in delta_range:
            print(f'=== delta {delta} ===')
            first_representative = ClassRepresentative(self, Image.open(first_img_path), delta)
            second_representative = ClassRepresentative(self, Image.open(second_img_path), delta)

            first_representative.solve_distances_matrix(second_representative)
            second_representative.solve_distances_matrix(first_representative)

            characteristics = first_representative.solve_characteristics(second_representative, "none")
            second_representative.solve_characteristics(first_representative, "none")

            kfe = np.max(first_representative.kfes)
            kfes.append(kfe)

            if kfe > optimal_kfe:
                optimal_kfe = kfe
                optimal_delta = delta

                with pd.ExcelWriter('after.xlsx') as writer:
                    characteristics.to_excel(writer, sheet_name='characteristics_1')



        print(optimal_kfe, optimal_delta)

        ax2.plot(delta_range, kfes)
        ax2.scatter(optimal_delta, optimal_kfe, c='red')

        plt.show()
