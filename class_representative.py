from PIL import Image
from TK_element import ArrayElement, ImageElement
from accessify import private
from sklearn.metrics import confusion_matrix

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

        gray_image = np.array(image)[:, :, 0]
        gray_matrix = (gray_image * 255).astype(int)

        mean = gray_image.mean(axis=0)
        uthres = mean + binary_threshold
        lthres = mean - binary_threshold
        binary_matrix = ((gray_image > lthres) & (gray_image < uthres)).astype(int)

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

    # def solve_kfe(self):
    #
    #     mat1 = self._distance_matrix.array
    #     mat2 = None
    #
    #     print(mat1.flatten().shape)
    #
    #     d = np.arange(0, 72 + 1)
    #
    #     c_pred = mat1.flatten() < d[:, None]
    #     print(c_pred.shape)
    #     c_true = np.concatenate((np.full(fill_value=True, shape=mat1.shape[1]),
    #                              np.full(fill_value=False, shape=mat1.shape[1])))
    #
    #     table = np.apply_along_axis(lambda y_pred: confusion_matrix(y_pred, c_true).reshape(4), 1, c_pred) / mat1.shape[
    #         1]
    #
    #     alpha = table[:, 2]
    #     beta = table[:, 3]
    #
    #     kfe = np.log((2 - alpha - beta) / (alpha + beta)) / np.log(2) * (1 - alpha - beta)
    #     print(f"!!!{kfe}")



# class ClassRepresentativeFactory:
#     @classmethod
#     def get_representatives_pair(
#             cls,
#             image,
#             other_image,
#             binary_delta: float,
#             other_binary_delta: float,
#     ):
#         gray_image = np.array(image)
#         gray_matrix = (np.array(image) * 255).astype(int)[:, :, 0]
#         binary_matrix = (gray_matrix >= (binary_delta * 255)).astype(int)
#         binary_image = binary_matrix * 255
#         standard_vector = (binary_matrix.mean(axis=0) >= .5).astype(int)
#
#         other_gray_image = np.array(other_image)
#         other_gray_matrix = (np.array(other_gray_image) * 255).astype(int)[:, :, 0]
#         other_binary_matrix = (other_gray_matrix >= (other_binary_delta * 255)).astype(int)
#         other_binary_image = other_binary_matrix * 255
#         other_standard_vector = (other_binary_matrix.mean(axis=0) >= .5).astype(int)
#
#     @classmethod
#     @private
#     def get_gray_image(
#             cls,
#             standard_vector: np.ndarray,
#             binary_matrix: np.ndarray,
#             other_binary_matrix: np.ndarray
#     ):
#         pass
#
#     @classmethod
#     @private
#     def get_distance_matrix(
#             cls,
#             standard_vector: np.ndarray,
#
#     ):
