from PIL import Image
from TK_element import ArrayElement, ImageElement
from accessify import private
from sklearn.metrics import confusion_matrix

import numpy as np
import pandas as pd


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

    @property
    def kfes(self):
        return self._kfe.array

    def __init__(self, app, image: Image, binary_threshold: float):
        self._app = app

        gray_image = np.array(image)[:, :, 0]
        gray_matrix = (gray_image * 255).astype(int)

        mean = gray_image.mean(axis=0)
        uthres = mean + binary_threshold
        lthres = mean - binary_threshold
        binary_matrix = ((gray_image > lthres) & (gray_image < uthres)).astype(int)

        binary_image = binary_matrix * 255
        standard_vector = (binary_matrix.mean(axis=0) >= .65).astype(int)

        self._gray_image = ImageElement(app, gray_image)
        self._gray_matrix = ArrayElement(app, gray_matrix)
        self._binary_image = ImageElement(app, binary_image)
        self._binary_matrix = ArrayElement(app, binary_matrix)
        self._standard_vector = ArrayElement(app, standard_vector)
        self._distance_matrix = None
        self._kfe = None

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

    def solve_characteristics(self, other, excel_file_name: str):
        other: ClassRepresentative = other

        ### SOLVING BASE CHARACTERISTICS ###
        centroid_distance = (self._standard_vector.array != other._standard_vector.array).sum()
        distance_matrix = np.copy(self._distance_matrix.array)

        d = np.array([i for i in range(0, centroid_distance + 1)])
        # d = np.array([i for i in range(0, 100)])

        c_pred = distance_matrix.flatten() < d[:, None]
        c_true = np.concatenate((np.full(fill_value=True, shape=distance_matrix.shape[1]),
                                 np.full(fill_value=False, shape=distance_matrix.shape[1])))

        characteristics = np.apply_along_axis(
            lambda y_pred: confusion_matrix(y_pred, c_true).reshape(4),
            axis=1,
            arr=c_pred) / distance_matrix.shape[1]

        alpha = characteristics[:, 2]
        beta = characteristics[:, 1]
        d1 = characteristics[:, 0]
        d2 = characteristics[:, 3]

        kfe = np.where(
            (d1 >= 0.5) & (d2 >= 0.5),
            np.log((2 - alpha - beta) / (alpha + beta)) / np.log(2) * (1 - alpha - beta),
            0
        )
        self._kfe = ArrayElement(self._app, kfe)

        characteristics = np.concatenate((characteristics, kfe[:, None]), axis=1)

        characteristics = pd.DataFrame(characteristics, columns=['D1', 'Beta', 'Alpha', 'D2', 'KFE'])

        ### CHARACTERISTICS OPTIMIZATION ###

        with pd.ExcelWriter(f'{excel_file_name}.xlsx') as writer:
            characteristics.to_excel(writer, sheet_name='characteristics_1')

        return characteristics

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
