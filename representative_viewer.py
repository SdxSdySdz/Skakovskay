from TK_element import TK_Element
from class_representative import ClassRepresentative


class RepresentativeViewer:
    @classmethod
    def view(cls, representative: ClassRepresentative, column: int):
        i = 1
        for element in representative.view_order:
            cls.show_element(element, i, column)
            i += 1

    @staticmethod
    def show_element(element: TK_Element, row: int, column: int):
        element.init_label(row, column)
