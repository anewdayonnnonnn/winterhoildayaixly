import numpy as np

a = np.arange(0,12).reshape(3,4)

print(a.shape)  # 阵列
print(a.dtype)  # 元素类型
print(a.ndim)  # 轴数

a_T = a.T
a_T_1d = a_T.reshape(-1)

