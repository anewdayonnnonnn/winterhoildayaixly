import numpy as np
# 直接计算实现神经元
# 定义激活函数，为神经元输出做准备
def sigmoid(x):
    return 1/(1+np.exp(-x))

# 进行神经元的计算
def neuron_direct(x, w, b):
    z = 0
    for xi,wi in zip(x, w):
        z += xi * wi
    z += b
    return sigmoid(z)

# 测试
x = np.array([0.5, 0.3])
w = np.array([0.2, 0.4])
b = 0.1
print("直接计算结果:", neuron_direct(x, w, b))

# 矩阵方式实现神经元
def neuron_matrix(x, w, b):
    z = np.dot(x, w) + b
    return sigmoid(z)

# 测试
print("矩阵计算结果:", neuron_matrix(x, w, b))

# 由神经元组成网络，实现向前传播
# 2输入 3隐藏 1输出
# 输入层 -> 隐藏层
W1 = np.array([[0.1, 0.2],
               [0.3, 0.4],
               [0.5, 0.6]])  # 3x2
b1 = np.array([0.1, 0.2, 0.3])  # 3x1

# 隐藏层 -> 输出层
W2 = np.array([[0.7, 0.8, 0.9]])  # 1x3
b2 = np.array([0.4])  # 1x1

# 前向传播函数
def forward(x):
    # 输入 -> 隐藏
    z1 = np.dot(W1, x) + b1
    a1 = sigmoid(z1)

    # 隐藏 -> 输出
    z2 = np.dot(W2, a1) + b2
    a2 = sigmoid(z2)

    return a2


# 测试
x = np.array([0.5, 0.3])
output = forward(x)
print("网络前向传播结果:", output)