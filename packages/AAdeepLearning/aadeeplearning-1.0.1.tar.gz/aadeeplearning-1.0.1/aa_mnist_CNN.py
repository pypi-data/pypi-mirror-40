from __future__ import print_function
import numpy as np

np.random.seed(1337)
# 生产环境
from aa_deep_learning.aadeeplearning import AADeepLearning
from aa_deep_learning.aadeeplearning.datasets import mnist
from aa_deep_learning.aadeeplearning.datasets import np_utils

# 测试环境
# from aadeeplearning import aadeeplearning as aa

# 输入图像的维度，此处是mnist图像，因此是28*28
img_rows, img_cols = 28, 28
# 10分类
nb_classes = 10

# keras中的mnist数据集已经被划分成了60,000个训练集，10,000个测试集的形式，按以下格式调用即可
(X_train, y_train), (X_test, y_test) = mnist.load_data()
X_test = X_test[:64]
y_test = y_test[:64]

# print(X_test[0])

# 画出minist 数字
# import matplotlib.pyplot as plt
# fig = plt.figure()
# plt.imshow(X_test[0],cmap = 'binary')#黑白显示
# plt.show()

# 后端使用tensorflow时，即tf模式下，
# 会将100张RGB三通道的16*32彩色图表示为(100,16,32,3)，
# 第一个维度是样本维，表示样本的数目，
# 第二和第三个维度是高和宽，
# 最后一个维度是通道维，表示颜色通道数
X_train = X_train.reshape(X_train.shape[0], img_rows, img_cols, 1)
X_test = X_test.reshape(X_test.shape[0], img_rows, img_cols, 1)
input_shape = (img_rows, img_cols, 1)

# 将X_train, X_test的数据格式转为float32
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
# 归一化
X_train /= 255
X_test /= 255
# 打印出相关信息
print('X_train shape:', X_train.shape)
print('y_train shape:', y_train.shape)
print('X_test shape:', X_test.shape)
print('y_test shape:', y_test.shape)
print(X_train.shape[0], 'train samples')
print(X_test.shape[0], 'test samples')
# X_train shape: (60000, 28, 28, 1)
# 60000 train samples
# 10000 test samples

# 将类别向量(从0到nb_classes的整数向量)映射为二值类别矩阵，
# 相当于将向量用one-hot重新编码
Y_train = np_utils.to_categorical(y_train, nb_classes)
Y_test = np_utils.to_categorical(y_test, nb_classes)
# print(Y_test.shape)
# 网络配置文件
solver = {
    # 初始学习率
    "learning_rate": 0.001,
    # 学习率衰减: 通常设置为 0.99
    "learning_rate_decay": 0.9999,
    # 优化策略: sgd/momentum/rmsprop
    "optimizer": "momentum",
    # 如果想使用添加动量的梯度下降算法做优化,需要设置这一项，通常设置为 0.9/0.95 即可，一般不需要调整
    "momentum_coefficient": 0.95,
    # rmsprop优化器的衰减系数
    "rmsprop_decay": 0.95,
    # 正则化系数
    "reg_coefficient": 0,
    # 训练多少次
    "number_iteration": 8000,
    # 每次用多少个样本训练
    "batch_size": 64,
    # 每隔几个迭代周期评估一次准确率？
    "evaluate_interval": 10,
    # 是否更新学习率？  true/false
    "learning_rate_update": True,
    # 是否需要保存模型快照？ true/false
    "snapshot": False,
    # 每隔几个迭代周期保存一次快照？
    "snapshot_interval": 5,
    # 是否以fine_tune方式训练？ true/false
    "fine_tune": False,
    # 预训练参数模型所在路径
    "pre_train_model": "./iter5.gordonmodel"
}

net = [
    {
        # 层名
        "name": "convolutional_1",
        # 层类型
        "type": "convolutional",
        # 卷积核个数
        "kernel_number": 32,
        # 卷积核高
        "kernel_height": 5,
        # 卷积核宽
        "kernel_width": 5,
        # 填充数
        "padding": 1,
        # 滑动步长
        "stride": 1,
        # 权重初始化  gaussian/msra
        "weight_init": "msra"
    },
    {
        # 层名
        "name": "pooling_1",
        # 层类型（最大池化）
        "type": "pooling",
        # 池化核高
        "kernel_height": 3,
        # 池化核宽
        "kernel_width": 3,
        # 滑动步长
        "stride": 2
    },
    {
        # 层名
        "name": "relu_1",
        # 层类型
        "type": "relu"
    },
    {
        # 层名
        "name": "convolutional_2",
        # 层类型
        "type": "convolutional",
        # 卷积核个数
        "kernel_number": 32,
        # 卷积核高
        "kernel_height": 5,
        # 卷积核宽
        "kernel_width": 5,
        # 填充数
        "padding": 1,
        # 滑动步长
        "stride": 1,
        # 权重初始化  gaussian/msra
        "weight_init": "msra"
    },
    {
        # 层名
        "name": "relu_2",
        # 层类型
        "type": "relu"
    },
    {
        # 层名
        "name": "pooling_2",
        # 层类型
        "type": "pooling",
        # 池化核高
        "kernel_height": 3,
        # 池化核宽
        "kernel_width": 3,
        # 滑动步长
        "stride": 2
    },
    {
        # 层名
        "name": "fully_connected_1",
        # 层类型
        "type": "fully_connected",
        # 神经元个数
        "neurons_number": 256,
        # 权重初始化方式  msra/gaussian
        "weight_init": "msra"
    },
    {
        # 层名
        "name": "relu_1",
        # 层类型 可选，relu，sigmoid，tanh，
        "type": "relu",
        # relu函数的上界限制值；   注： 不做设置或者设置为0意味着是普通的relu函数
        "threshold": 0
    },
    # {
    #     # 层名
    #     "name": "drop1",
    #     # 层类型
    #     "type": "Dropout",
    #     # dropout比例（置零比例）
    #     "drop rate": 0.5
    # },
    {
        # 层名
        "name": "fully_connected_2",
        # 层类型
        "type": "fully_connected",
        # 神经元个数
        "neurons_number": 128,
        # 权重初始化方式  msra/gaussian
        "weight_init": "msra"
    },
    {
        # 层名
        "name": "relu_2",
        # 层类型
        "type": "relu",
        # relu函数的上界限制值；   注： 不做设置或者设置为0意味着是普通的relu函数
        "threshold": 0
    },
    {
        # 层名
        "name": "fully_connected_3",
        # 层类型
        "type": "fully_connected",
        # 神经元个数
        "neurons_number": 10,
        # 权重初始化方式  msra/gaussian
        "weight_init": "msra"
    },
    {
        # 层名
        "name": "softmax",
        # 层类型
        "type": "softmax"
    }
]

AA = AADeepLearning(solver, net)
# 训练模型
AA.train(X_train, Y_train, X_test, Y_test)

# 按batch计算在某些输入数据上模型的误差
score = AA.predict(X_test, Y_test)

"""
# 输出训练好的模型在测试集上的表现
print('Test score:', score[0])
print('Test accuracy:', score[1])

# Test score: 0.032927570413
# Test accuracy: 0.9892
"""
