"""Contains the base Layer class, from which all layers inherit.
"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

class Layer(object):
    def __init__(self):
        pass
    def init(self, neural_net,input_shape):
        pass
    def forward(self):
        pass
    def backward(self):
        pass
