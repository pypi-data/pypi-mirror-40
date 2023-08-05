"""Contains the base Layer class, from which all layers inherit.
"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import numpy as np


class SoftMax():
    @staticmethod
    def init(layer):
        return layer
    @staticmethod
    def forword(flow_data, config):
        for i in range(config['batch_size']):
            flow_data[:, i] = np.exp(flow_data[:, i]) / np.sum(np.exp(flow_data[:, i]))
        return flow_data
    @staticmethod
    def backword(flow_data, label):
        # 获取最末层误差信号 softmax反向传播
        return flow_data - label.T
