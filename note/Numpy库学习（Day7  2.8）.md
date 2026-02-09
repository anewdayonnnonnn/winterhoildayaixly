# Numpy库学习（Day7  2.8）

### Numpy基础了解

Numpy提供了多维数组的结构，是python中用于科学计算和数字处理的核心库

- **基础数组创建**

  - ```
    # 一维数组创建
    import numpy as np
    a = np.array([2, 3, 4])  # 注意：array中的元素都必须要以列表形式存在
    						 # 错误：a = np.array(1, 2, 3, 4）
    
    #二维数组创建
    b = np.array([[1, 2],[3, 4]])  # tip:几维几层[]
    
    # 创建时显示指定数组类型
    c = np.array([[1, 2], [3, 4]], dtype=complex)
    ```

  - ```
    """ 包含初始占位符内容数组生成 """
    import numpy as np
    # 初始化0
    np.zeros((3,4))
    
    # 初始化1
    np.ones((2, 3, 4))
    
    # 初始化随机
    np.empty((2, 3))
    ```

  - ```
    # 以步长创建数组
    import numpy as np
    np.arange(10, 30, 5) 
    
    # 以元素个数创建数组
    from numpy import pi
    np.linspace(0, 2, 9)  # 浮点数更适用这种，不会因精度而损失元素个数
    ```

- **特殊数组创建**

  - ```
    import numpy as np
    
    # 单位矩阵（主对角线为1）
    a = np.identity(n)  # 构建 n*n的单位矩阵
    b = np.eye(n,k=0)  # k=0 是主对角线，默认值
    
    # 随机矩阵（均匀分布/正态分布）
    # 均匀分布随机矩阵
    a = np.random.rand(2, 3)  # 2行3列，值在[0, 1)
    b = np.random.randint(low=1,high=11,size=(2,3))
    # 正态分布随机矩阵
    c = np.random.randn(2, 3)  # 标准正态分布（均值0，方差1）
    np.random.seed(42)
    d =  np.random.randn(2, 3)  # 用随机数种子确保每次运行结果一致
    
    # 对角矩阵
    a = [1, 2, 3]
    b = np.diag(a)  # 3 * 3对角矩阵，对角线为1，2，3
    ```

### Numpy矩阵操作

- **矩阵乘法**：

  - 逐元素相乘：*

  - 矩阵点积（真正数学矩阵乘）：np.dot/@

  - ```
    import numpy as np 
    A = np.array([[1, 2],[3, 4]])
    B = np.array([[5, 6],[7, 8]])
    
    # 逐元素相乘
    D1 = A * B
    D1 = np.multiply(A, B)
    
    #矩阵点积
    D2 = A @ B
    D2 = np.dot(A, B)
    
    ```

- **矩阵广播**：广播**只用于逐元素计算**

  - 核心规则：1.维度相同，不足补1  2.维度兼容，对齐后相应位置要一个为1或相等

  - ```
    import numpy as np
    
    A = np.ones((3,4))    # 形状 (3,4)
    B = np.array([1,2,3,4]) # 形状 (4,)
    
    # 结果
    [1,2,3,4]
    [1,2,3,4]
    [1,2,3,4]
    ```

- **矩阵转置**：将矩阵行和列互换

  - ```
    import numpy as np
    
    A = np.array([[1, 2, 3],[4, 5, 6]])
    
    # 方法1
    A_T = A.T
    
    # 方法2
    A_T = np.transpose(A)
    # 等价写法
    A_T = A.transpose()
    ```

- 矩阵的逆：非方阵没有逆矩阵

  - ```
    import numpy as np
    
    A = np.array([[1, 2, 3],[4, 5, 6]])
    
    A_inv = np.linalg.inv(A)
    ```

- 矩阵存取：索引从0开始

  - ```
    import numpy as np
    
    mat = np.array([
        [1, 2, 3, 4],   
        [5, 6, 7, 8],   
        [9, 10, 11, 12] 
    ])
    
    # 读取元素
    # 方式1：取单个元素（行索引, 列索引）
    elem = mat[1, 2]  
    print("\n单个元素 mat[1,2]：", elem)
    
    # 方式2：取整行（行索引, :）
    row_1 = mat[1, :]
    print("整行 mat[1,:]：", row_1) 
    
    # 方式3：取整列（:, 列索引）
    col_2 = mat[:, 2]
    print("整列 mat[:,2]：", col_2)  
    
    # 方式4：取区域（切片）
    region = mat[0:2, 1:3]
    print("区域 mat[0:2,1:3]：\n", region)
    
    # 存取元素
    # 方式1：给单个元素赋值
    mat[1, 2] = 99  
    print("\n赋值后 mat[1,2]=99：\n", mat)
    
    # 方式2：给整行赋值
    mat[2, :] = [0, 0, 0, 0]  
    print("赋值后 mat[2,:]=[0,0,0,0]：\n", mat)
    
    # 方式3：给区域赋值
    mat[0:2, 1:3] = 88  # 把前2行、第2-3列的区域都改成88
    print("赋值后 mat[0:2,1:3]=88：\n", mat)
    
    # 此外，还有按条件存取和多维索引（一次性取不连续的元素）
    ```

### 矩阵属性

- ndarray.ndim  数组的轴数（维度）

- ndarray.shape  阵列的尺寸   

  - ```
    arr1 = np.array([1, 2, 3, 4])  
    print(arr1.shape)  # (4,)
    ```

- ndarray.size  数组的总元素数
- ndarray.dtype  数组中元素类型的对象
-  ndarray.itemsize  数组中每个元素的字节大小
- ndarray.data 缓冲区包含数组的实际元素

### 补充

- reshape：将数组展开成一维后再转换成另一种形状，与转置不同

  - -1：自动推算维度，如（2，3，5）的矩阵 要写（5，3，-1）/转成1维，只要写一个-1

    



