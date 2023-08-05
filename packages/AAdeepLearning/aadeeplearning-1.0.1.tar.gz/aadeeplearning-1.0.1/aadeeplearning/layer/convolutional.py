"""Contains the base Layer class, from which all layers inherit.
"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import numpy as np


class Convolutional():
    @staticmethod
    def init(layer, input_shape):
        # 何凯明初始化，主要针对relu激活函数
        # if layer["weight_init"] == 'msra':
        #     layer["weight"] = np.random.randn(layer['neurons_number'],
        #                                       input_shape) * (np.sqrt(2/input_shape))
        # # xavier，主要针对tanh激活函数
        # elif layer["weight_init"] == 'xavier':
        #     layer["weight"] = np.random.randn(layer['neurons_number'],
        #                                       input_shape) * (np.sqrt(1/input_shape))
        # else:
        #     layer["weight"] = np.random.randn(layer['neurons_number'], input_shape) * 0.01
        layer["weight"] = np.random.randn(layer['kernel_width'], layer['kernel_height']) * 0.01
        layer["bias"] = np.zeros((layer['kernel_width'], layer['kernel_height']))
        return layer, input_shape
    @staticmethod
    def forword(layer, flow_data):
        # Z = np.dot(layer['weight'], flow_data) + layer['bias']
        return flow_data
    @staticmethod
    def backword(flow_data, layer, config):
        # layer["weight_gradient"] = (1 / config['batch_size']) * np.dot(flow_data, layer['input'].T)
        # layer["bias_gradient"] = (1 / config['batch_size']) * np.sum(flow_data, axis=1, keepdims=True)
        # flow_data = np.dot(layer['weight'].T, flow_data)
        return layer, flow_data
