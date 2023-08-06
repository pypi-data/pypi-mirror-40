"""Training-related part of the Keras engine.
"""
# from __future__ import absolute_import
# from __future__ import division
# from __future__ import print_function
#
# import warnings
# import copy
import numpy as np
from .layer.fully_connected import FullyConnected
from .layer.relu import Relu
from .layer.softmax import SoftMax
from .layer.convolutional import Convolutional
from .layer.pooling import Pooling
import matplotlib.pyplot as plt

"""
如果每一层神经元的尺寸如下：
weight_1.shape： (256, 784)
bias_1.shape： (256, 1)
weight_2.shape： (128, 256)
bias_2.shape： (128, 1)
weight_3.shape： (10, 128)
bias_3.shape： (10, 1)

那么数据前向传播和反向传播尺寸的变化情况如下

第1层，前向传播输出数据尺寸： (256, 64)  =    神经元尺寸 (256, 784) *数据尺寸(784,64)
第2层，前向传播输出数据尺寸： (128, 64)  =     神经元尺寸 (128, 256)*数据尺寸(256, 64)
第3层，前向传播输出数据尺寸： (10, 64)    =      神经元尺寸  (10, 128) *数据尺寸(128, 64)

第3层，因为是从softmax层回传过来的，尺寸不变 (10, 64)
第2层，反向传播输出数据尺寸： (128, 64)  =   下一层weight 尺寸.T (128, 10)*流动数据尺寸(10, 64)
第1层，反向传播输出数据尺寸： (256, 64)  =   下一层weight尺寸.T (256, 128)*流动数据尺寸(128, 64)
"""

class AADeepLearning():
    config = None
    net = None
    # 初始化网络参数
    net = {}
    # 损失值
    loss = []
    # 训练数据 shape: (60000, 28, 28, 1)  (样本数, 宽, 高, 通道数)
    train_data = []
    # 训练数据标签
    train_label = []
    # 损失值
    test_data = []
    # 损失值
    test_lable = []
    # 损失值
    input_shape = 0
    # 学习率
    learning_rate = 0
    # 神经网络层数
    layer_number = 0
    # 神经网络参数 weight和bias
    net = {}

    def __init__(self, config, net):
        self.config = config
        self.net = net
        # 网络结构和定义层一致
        self.net = net
        self.learning_rate = config['learning_rate']

    def train(self, train_data, train_label, test_data, test_label):
        # 宽*高*通道数
        self.input_shape = train_data.shape[1] * train_data.shape[2] * train_data.shape[3]
        # 1，初始化网络参数
        net = self.init_parameters()
        loss_list = []
        for iteration in range(self.config['number_iteration']):
            train_data_batch, train_label_batch = self.next_batch(train_data, train_label, self.config['batch_size'])
            # 2，前向传播
            flow_data = self.forward_pass(net, train_data_batch)
            # 3，计算损失
            loss = self.compute_cost(flow_data, train_label_batch)
            loss_list.append(loss)
            # 4，反向传播，求梯度
            net = self.backward_pass(net, flow_data, train_label_batch)
            # 5，根据梯度更新一次参数
            net = self.update_parameters(net)
            if iteration % 100 == 0:
                # self.check_weight(gradient, cache)
                print('iteration:', iteration, 'loss:', loss)
        self.net = net
        # plt.plot(loss_list, 'r')
        # plt.xlabel("iteration")
        # plt.ylabel("loss")
        # plt.show()

    def init_parameters(self):
        net = self.net
        # 第一层的输出尺寸就是数据尺寸
        output_shape=self.input_shape
        for i, layer in enumerate(net):
            if layer['type'] == 'convolutional':
                net[i], output_shape = Convolutional.init(layer=layer, input_shape=output_shape)
            elif layer['type'] == 'fully_connected':
                net[i], output_shape = FullyConnected.init(layer=layer, input_shape=output_shape)
        for i, layer in enumerate(net):
            if layer['type'] == 'fully_connected':
                print(layer['name']+",weight.shape：", layer["weight"].shape)
                print(layer['name']+",bias.shape：", layer["bias"].shape)
        return net

    def forward_pass(self, net, data):
        # X_train shape: (60000, 28, 28, 1) ——> (784, 60000)
        # 流动数据，一层一层的计算，并先后流动
        flow_data = data.reshape(data.shape[0], -1).T
        for i, layer in enumerate(net):
            # 缓存当前层的输入
            net[i]['input'] = flow_data
            if layer['type'] == 'convolutional':
                flow_data = Convolutional.forword(layer=layer, flow_data=flow_data)
            elif layer['type'] == 'pooling':
                flow_data = Pooling.forword(layer=layer, flow_data=flow_data)
            elif layer['type'] == 'fully_connected':
                flow_data = FullyConnected.forword(layer=layer, flow_data=flow_data)
            elif layer['type'] == 'relu':
                flow_data = Relu.forword(flow_data=flow_data)
            elif layer['type'] == 'softmax':
                flow_data = SoftMax.forword(flow_data=flow_data, config=self.config)
            # 缓存当前层的输出
            net[i]['output'] = flow_data
        return flow_data

    def compute_cost(self, layer_output, batch_label):
        batch_size = self.config['batch_size']
        loss = 0.0
        for i in range(batch_size):
            loss += -np.sum(np.dot(batch_label[i], np.log(layer_output[:, i])))
        loss = loss / batch_size
        return loss

    def backward_pass(self, net, flow_data, train_label):
        layer_number = len(net)
        for i in reversed(range(0, layer_number)):
            layer = net[i]
            if layer['type'] == 'convolutional':
                net[i], flow_data = Convolutional.backword(flow_data=flow_data, layer=layer, config=self.config)
            elif layer['type'] == 'pooling':
                flow_data = Pooling.backword(flow_data=flow_data, layer=layer, config=self.config)
            elif layer['type'] == 'fully_connected':
                net[i], flow_data = FullyConnected.backword(flow_data=flow_data, layer=layer, config=self.config)
            elif layer['type'] == 'relu':
                # print(layer["name"], flow_data.shape, layer["output"].shape)
                # exit()
                flow_data = Relu.backword(flow_data=flow_data, layer=layer)
            elif layer['type'] == 'softmax':
                flow_data = SoftMax.backword(flow_data=flow_data, label=train_label)
        return net

    def update_parameters(self, net):

        for i, layer in enumerate(net):
            # if layer['type'] == 'fully_connected' or layer['type'] == 'convolutional':
            if layer['type'] == 'fully_connected':
                net[i]["weight"] = net[i]["weight"] - self.learning_rate * net[i]["weight_gradient"]
                net[i]["bias"] = net[i]["bias"] - self.learning_rate * net[i]["bias_gradient"]
        return net

    def predict(self, test_data, test_label):
        flow_data = self.forward_pass(self.net, test_data)
        flow_data = np.array(flow_data).T
        batch_size = flow_data.shape[0]
        right = 0
        for i in range(0, batch_size):
            index = np.argmax(flow_data[i])
            if test_label[i][index] == 1:
                right += 1
        accuracy = right / batch_size
        print(accuracy)
        return accuracy

    def flatten_layer(self):
        self.train_data = []

    def ReLU(self, input):
        return np.maximum(0, input)

    def sigmoid(self, input):
        return 1 / (1 + np.exp(-input))

    def tanh(self, Z):
        return np.tanh(Z)

    def next_batch(self, train_data, train_label, batch_size):
        index = [i for i in range(0, len(train_label))]
        np.random.shuffle(index)
        batch_data = []
        batch_label = []
        for i in range(0, batch_size):
            batch_data.append(train_data[index[i]])
            batch_label.append(train_label[index[i]])
        batch_data = np.array(batch_data)
        batch_label = np.array(batch_label)
        return batch_data, batch_label
    def check_weight(self, gradient, cache):
        for i in range(1, self.layer_number+1):
            print("Z_"+str(i)+"[:,1]_mean =", np.mean(cache["Z_"+str(i)][:, 1]), "; Z1[:,1]_std =",
                  np.std(cache["Z_"+str(i)][:, 1]))  # 统计某一列激活值的均值和标准差
            print("A"+str(i)+"[:,1]_mean =", np.mean(cache["A_"+str(i)][:, 1]), "; A1[:,1]_std =",
                  np.std(cache["A_"+str(i)][:, 1]))  # 统计某一列激活值的均值和标准差
            print("|dW"+str(i)+"|<1e-8 :", np.sum(abs(gradient["d_weight_"+str(i)]) < 1e-8), "/",
                  gradient["d_weight_"+str(i)].shape[0] * gradient["d_weight_"+str(i)].shape[1])
