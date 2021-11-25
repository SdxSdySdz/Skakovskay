from PIL import Image
from TK_element import ArrayElement, ImageElement

import numpy as np


class ClassRepresentative:
    @property
    def view_order(self):
        return [
            self._gray_image,
            self._gray_matrix,
            self._binary_image,
            self._binary_matrix,
            self._standard_vector,
            self._distance_matrix,
        ]

    def __init__(self, app, image: Image, binary_threshold: float):
        self._app = app

        gray_image = np.array(image)
        gray_matrix = (np.array(image) * 255).astype(int)[:, :, 0]
        binary_matrix = (gray_matrix >= (binary_threshold * 255)).astype(int)
        binary_image = binary_matrix * 255
        standard_vector = (binary_matrix.mean(axis=0) >= .5).astype(int)

        self._gray_image = ImageElement(app, gray_image)
        self._gray_matrix = ArrayElement(app, gray_matrix)
        self._binary_image = ImageElement(app, binary_image)
        self._binary_matrix = ArrayElement(app, binary_matrix)
        self._standard_vector = ArrayElement(app, standard_vector)
        self._distance_matrix = None

    def solve_distances_matrix(self, other):
        other: ClassRepresentative = other

        if self._binary_matrix.array.shape != other._binary_matrix.array.shape:
            raise ValueError("")

        distances_matrix = np.zeros((2, self._standard_vector.shape[0]))

        first_mismatches_matrix = np.apply_along_axis(
            arr=self._binary_matrix.array,
            func1d=lambda line: line ^ self._standard_vector.array,
            axis=1
        )

        second_mismatches_matrix = np.apply_along_axis(
            arr=other._binary_matrix.array,
            func1d=lambda line: line ^ self._standard_vector.array,
            axis=1
        )

        distances_matrix[0] = np.sum(first_mismatches_matrix, axis=1)
        distances_matrix[1] = np.sum(second_mismatches_matrix, axis=1)

        self._distance_matrix = ArrayElement(self._app, distances_matrix.astype(int))
