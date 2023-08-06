import numpy as np

from lfa_toolbox.core.mf.free_shape_mf import FreeShapeMF


class SingletonMF(FreeShapeMF):
    """
    Syntactic sugar to create a singleton output fuzzy set
    """

    def __init__(self, in_value):
        super(SingletonMF, self).__init__(mf_values=[1], in_values=[in_value])

    def fuzzify(self, in_value: float):
        print(
            "[warning] fuzzify a singleton value is maybe not the thing you "
            "want to do"
        )
        return 1 if np.isclose(self.in_values[0], in_value) else 0
