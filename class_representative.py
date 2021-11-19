from PIL import Image
from TK_element import TK_Element, ArrayElement, ImageElement

import numpy as np


class ClassRepresentative:
    @property
    def view_order(self):
        return self._view_order

    def __init__(self, app, image: Image, binary_threshold: float):
        gray_image = np.array(image)
        gray_matrix = (np.array(image) * 255).astype(int)[:, :, 0]
        binary_matrix = (gray_matrix >= (binary_threshold * 255)).astype(int)
        binary_image = binary_matrix * 255
        standard_vector = (binary_matrix.mean(axis=0) >= .5).astype(int)
        # distances_matrix = np.zeros((2, len(gray_matrix)))

        self._gray_image = ImageElement(app, gray_image)
        self._gray_matrix = ArrayElement(app, gray_matrix)
        self._binary_image = ImageElement(app, binary_image)
        self._binary_matrix = ArrayElement(app, binary_matrix)
        self._standard_vector = ArrayElement(app, standard_vector)

        self._view_order = [
            self._gray_image,
            self._gray_matrix,
            self._binary_image,
            self._binary_matrix,
            self._standard_vector,
        ]
