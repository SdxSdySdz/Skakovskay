from PIL import Image
from TK_element import TK_Element, ArrayElement, ImageElement

import numpy as np


class ImageInfo:
    def __init__(self, app, image: Image, binary_threshold: float):
        self._gray_image = ImageElement(app, np.array(image))
        self._gray_matrix = ArrayElement(app, (np.array(image) * 255).astype(int)[:, :, 0])
        self._binary_matrix = ArrayElement(app, (self._gray_matrix.array >= (binary_threshold * 255)).astype(int))
        self._binary_image = ImageElement(app, self._binary_matrix.array * 255)
        self._standard_vector = ArrayElement(app, self._binary_matrix.array.mean(axis=0))

    def show(self, column: int):
        self.show_element(self._gray_image, 1, column)
        self.show_element(self._gray_matrix, 2, column)
        self.show_element(self._binary_image, 3, column)
        self.show_element(self._binary_matrix, 4, column)
        self.show_element(self._standard_vector, 5, column)

    @staticmethod
    def show_element(element: TK_Element, row: int, column: int):
        element.init_label(row, column)
