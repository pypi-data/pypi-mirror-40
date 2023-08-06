"""
This file implements the class that represents the cache of a layer during forward and backward
propagations
"""
from typing import Union
import numpy as np


class LayerCache:

    def __init__(self):
        self.preactivation: np.array = None
        self.activation: np.array = None

        # d_preactivation is the derivative of the cost function on the preactivation vector
        self.d_preactivation: np.array = None
        # d_W and d_b are the derivatives of the cost function on W and b respectively
        self.d_W: Union[np.array, float] = None
        self.d_b: Union[np.array, float] = None

        # forward_vector is the vector on which we have computed the forward propagation
        self.forward_vector = None
