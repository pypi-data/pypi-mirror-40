"""Training-related part of the Keras engine.
"""
# from __future__ import absolute_import
# from __future__ import division
# from __future__ import print_function
#
# import warnings
# import copy
import numpy as np
from .layer import *
import matplotlib.pyplot as plt


class AADeepLearning():
    solver = None
    net = None
    # 初始化网络参数
    net_parameters = {}
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
    neural_net = {}

    def __init__(self, solver, net):
        self.solver = solver
        self.net = net
        # 网络结构和定义层一致
        self.net_parameters = net
        self.learning_rate = solver['learning_rate']

    def train(self, train_data, train_label, test_data, test_label):
        # todo 数据量太大会占用太多内存
        self.train_data = train_data
        self.train_label = train_label
        self.test_data = test_data
        self.test_lable = test_label
        # 宽*高*通道数
        self.input_shape = self.train_data.shape[1] * self.train_data.shape[2] * self.train_data.shape[3]
        # 1，初始化网络参数
        neural_net = self.init_parameters()
        loss_list = []
        for iteration in range(self.solver['number_iteration']):
            train_data_batch, train_label_batch = self.next_batch(train_data, train_label, self.solver['batch_size'])
            # print
            # 2，前向传播
            layer_output, cache = self.forward_pass(neural_net, train_data_batch)
            # 3，计算损失
            loss = self.compute_cost(layer_output, train_label_batch)
            loss_list.append(loss)
            # 4，反向传播，求梯度
            gradient = self.backward_pass(neural_net, layer_output, cache, train_label_batch)
            # gradient_check()
            # 5，根据梯度更新一次参数
            neural_net = self.update_parameters(gradient, neural_net)
            if iteration % 100 == 0:
                # self.check_weight(gradient, cache)
                print('iteration:', iteration, 'loss:', loss)
        self.neural_net = neural_net
        # plt.plot(loss_list, 'r')
        # plt.xlabel("iteration")
        # plt.ylabel("loss")
        # plt.show()

    def init_parameters(self):
        # 上一层的输入尺寸
        front_layer_output_shape = self.input_shape
        neural_net = {}
        i = 0
        for key, value in enumerate(self.net_parameters):
            if value['type'] == 'fully_connected':
                i += 1
                # 何凯明初始化，主要针对relu激活函数
                if "weight_init" in value.keys() and value["weight_init"] == 'msra':
                    neural_net["weight_" + str(i)] = np.random.randn(value['neurons_number'],
                                                                 front_layer_output_shape) * (np.sqrt(2/front_layer_output_shape))
                # xavier，主要针对tanh激活函数
                elif "weight_init" in value.keys() and value["weight_init"] == 'xavier':
                    neural_net["weight_" + str(i)] = np.random.randn(value['neurons_number'],
                                                                 front_layer_output_shape) * (np.sqrt(1/front_layer_output_shape))
                else:
                    neural_net["weight_" + str(i)] = np.random.randn(value['neurons_number'],
                                                                 front_layer_output_shape) * 0.01
                neural_net["bias_" + str(i)] = np.zeros((value['neurons_number'], 1))
                # 权重
                # self.net_parameters[key]['weight'] = np.random.randn(value['neurons_number'],front_layer_output_shape)
                # 偏置参数
                # self.net_parameters[key]['bias'] = np.ones((value['neurons_number'], 1))
                front_layer_output_shape = value['neurons_number']
            elif value['type'] == 'relu' or value['type'] == 'sigmoid' or value['type'] == 'tanh':
                neural_net["active_" + str(i)] = value['type']
            elif value['type'] == 'softmax':
                neural_net["output_" + str(i)] = value['type']
        self.layer_number = i
        for i in range(1, self.layer_number + 1):
            print("weight_" + str(i) + ".shape：", neural_net["weight_" + str(i)].shape)
            print("bias_" + str(i) + ".shape：", neural_net["bias_" + str(i)].shape)
        return neural_net

    def forward_pass(self, neural_net, data):
        # X_train shape: (60000, 28, 28, 1) ——> (784, 60000)
        data = data.reshape(data.shape[0], -1).T
        A = data
        cache = {}
        cache["A_0"] = A
        for i in range(1, self.layer_number + 1):
            Z = np.dot(neural_net['weight_' + str(i)], A) + neural_net['bias_' + str(i)]
            if "active_" + str(i) in neural_net.keys() and neural_net["active_" + str(i)] == 'relu':
                A = self.ReLU(Z)
            elif "active_" + str(i) in neural_net.keys() and neural_net["active_" + str(i)] == 'sigmoid':
                A = self.sigmoid(Z)
            elif "active_" + str(i) in neural_net.keys() and neural_net["active_" + str(i)] == 'tanh':
                A = self.tanh(Z)
            else:
                # 没有激活函数
                A = Z

            cache["Z_" + str(i)] = Z
            cache["A_" + str(i)] = A

            if "output_" + str(i) in neural_net.keys() and neural_net["output_" + str(i)] == 'softmax':
                for j in range(self.solver['batch_size']):
                    A[:, j] = np.exp(A[:, j]) / np.sum(np.exp(A[:, j]))

            # print("第"+str(i)+"层，反向传播输出数据尺寸：", Z.shape,"第"+str(i)+"层，前向传播输出数据尺寸：",  cache["A_" + str(i)].shape)
        # Z = np.dot(neural_net['weight_' + str(self.layer_number)], A) + neural_net['bias_' + str(self.layer_number)]
        # A = self.ReLU(Z)
        # cache["Z_"+str(self.layer_number)] = Z
        # cache["A_"+str(self.layer_number)] = A
        # 最后的softmax
        return A, cache

    def compute_cost(self, layer_output, batch_label):
        # print(layer_output.shape)
        # print(batch_label.shape)
        # exit()
        batch_size = self.solver['batch_size']
        loss = 0.0
        for i in range(batch_size):
            loss += -np.sum(np.dot(batch_label[i], np.log(layer_output[:, i])))
        loss = loss / batch_size
        return loss

    def backward_pass(self, neural_net, layer_output, cache, train_label):
        """
        反向传播
        :param layer_output: 前向传播的输出
        :return:
        """
        gradient = {}  # 保存各层参数梯度的字典
        # 获取最末层误差信号 softmax反向传播
        dZL = layer_output - train_label.T
        gradient["d_weight_" + str(self.layer_number)] = (1 / self.solver['batch_size']) * np.dot(dZL, cache[
            "A_" + str(self.layer_number - 1)].T)
        gradient["d_bias_" + str(self.layer_number)] = (1 / self.solver['batch_size']) * np.sum(dZL, axis=1,
                                                                                                keepdims=True)

        for i in reversed(range(1, self.layer_number)):

            dZL = np.dot(neural_net['weight_' + str(i + 1)].T, dZL)

            print("第" + str(i) + "层，反向传播输出数据尺寸：", dZL.shape, "第" + str(i) + "层，前向传播输出数据尺寸：", cache["A_" + str(i)].shape)
            if "active_" + str(i) in neural_net.keys() and neural_net["active_" + str(i)] == 'relu':
                # print(i, dZL.shape, cache["A_" + str(i)].shape)
                # drelu/dz  = 小于零就始终等于0 ，大于0就等于一
                dZL = dZL * np.array(cache["A_" + str(i)] > 0)
            elif "active_" + str(i) in neural_net.keys() and neural_net["active_" + str(i)] == 'sigmoid':
                # dsigmoid/dz  = a*(1-a)
                dZL = dZL * (cache["A_" + str(i)] * (1 - cache["A_" + str(i)]))
            elif "active_" + str(i) in neural_net.keys() and neural_net["active_" + str(i)] == 'tanh':
                # dtanh/dz  = 1-a^2
                dZL = dZL * (1 - np.power(cache["A_" + str(i)], 2))

            gradient["d_weight_" + str(i)] = (1 / self.solver['batch_size']) * np.dot(dZL, cache["A_" + str(i - 1)].T)
            gradient["d_bias_" + str(i)] = (1 / self.solver['batch_size']) * np.sum(dZL, axis=1, keepdims=True)
        return gradient

    def update_parameters(self, gradient, neural_net):
        for index in range(1, self.layer_number + 1):
            neural_net['weight_' + str(index)] = neural_net['weight_' + str(index)] - self.learning_rate * gradient[
                'd_weight_' + str(index)]
            neural_net['bias_' + str(index)] = neural_net['bias_' + str(index)] - self.learning_rate * gradient[
                'd_bias_' + str(index)]
        return neural_net

    # def evaluate(self, test_data, test_label):
    #     print("evaluate")

    def predict(self, test_data, test_label):
        forward_output, _ = self.forward_pass(self.neural_net, test_data)
        forward_output = np.array(forward_output).T
        # print(forward_output.T.shape)
        # print(forward_output.T[0])
        batch_size = forward_output.shape[0]
        # p = np.zeros(test_label.shape)
        right = 0
        for i in range(0, batch_size):
            index = np.argmax(forward_output[i])
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
