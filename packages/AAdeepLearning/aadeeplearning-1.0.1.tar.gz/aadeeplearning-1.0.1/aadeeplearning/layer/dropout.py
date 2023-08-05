"""Contains the base Layer class, from which all layers inherit.
"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import copy
import re
from six.moves import zip

# from .. import backend as K
# from .. import initializers


class Layer(object):

    def __init__(self, **kwargs):
        self.input_spec = None

    @staticmethod
    def _node_key(layer, node_index):
        """Converts a layer and its index to a unique (immutable type) name.

        This function is used internally with `self._network_nodes`.

        # Arguments
            layer: The layer.
            node_index: The layer's position (e.g. via enumerate) in a list of
                nodes.

        # Returns
            The unique name.
        """
        return layer.name + '_ib-' + str(node_index)

    @property
    def losses(self):
        return self._losses

    @property
    def updates(self):
        if not self.trainable and not self.stateful:
            return []
        return self._updates

    @property
    def built(self):
        return self._built

    @built.setter
    def built(self, value):
        self._built = value

    @property
    def trainable_weights(self):
        trainable = getattr(self, 'trainable', True)
        if trainable:
            return self._trainable_weights
        else:
            return []

    @trainable_weights.setter
    def trainable_weights(self, weights):
        self._trainable_weights = weights
