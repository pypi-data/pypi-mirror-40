"""Contains the base Layer class, from which all layers inherit.
"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import numpy as np


class Relu():
    @staticmethod
    def init(layer):
        return layer
    @staticmethod
    def forword(flow_data):
        return np.maximum(0, flow_data)
    @staticmethod
    def backword(flow_data, layer):
        # drelu/dz  = 小于零就始终等于0 ，大于0就等于一
        return flow_data * np.array(layer["output"] > 0)
