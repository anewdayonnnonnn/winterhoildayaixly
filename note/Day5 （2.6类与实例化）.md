# Day5 （2.6类与实例化）

### 1.类与实例化

- 类：类是创建对象的“模板”，封装了对象的属性（数据）和方法（行为），描述了一类事物的共同特征

- 示例：

  ```python
  class Shape:  # 定义图形类（模板）
      shape_count = 0  # 类属性：所有实例共享
      
      def __init__(self)  # 初始化实例
          self.__area = None  # 实例属性：每个实例都有
  ```

- 实例：类的具体实现，是根据类模板创建的“具体对象”，每个实例又有自己独立的属性的方法

- 示例：

  ```python
  circle = Circle(5)  # 创建circle实例
  rectangle = Rectangle(4, 6)  # 创建Rectangle实例
  ```

### 2.类变量与实例变量

| 类型     | 归属           | 定义的位置                   | 访问方式                  | 特点                             |
| -------- | -------------- | ---------------------------- | ------------------------- | -------------------------------- |
| 类变量   | 类本身         | 类内部，但在所有方法之外     | 类名. 变量名或实例.变量名 | 所有实例共享，修改会影响所有实例 |
| 实例变量 | 单个实例所具有 | ——init——方法或其他实例方法内 | 实例.变量名               | 每个实例独立，互不影响           |

### 3.类方法

- 定义：属于类本身，并非实例，通过@classmethod修饰，第一个参数固定为cls（代表当前类）

- 示例：

  ```python
  @classmethod
  def get_shape_count(cls):
      """获取创建的图形总数"""
      return cls.shape_count
  print(Shape.get_shape_count())  # 直接通过类调用
  c = circle（1）  # 类调用不用先生成图形
  print(c.get_shape_count())  # 直接通过实例调用
  ```

- 核心特点：
  - 无法直接访问实例属性，只能操作类属性
  - 常见于批量生成实例

- 拓展： 1.静态方法（@staticmethod）

  - 定义：和类关联的普通函数，无默认参数

  - ```python
    class MathTool:
        @staticmethod
        def add(a, b):
            return a + b
    
    # 调用
    print(MathTool.add(1, 2))  # 类直接调用
    mt = MathTool()
    print(mt.add(3, 4))        # 实例调用
    ```

  - 核心特点：
    - 无 `self`/`cls` 参数，无法直接访问类 / 实例属性；
    - 仅仅作为类的工具函数，逻辑上属于类但不依赖类的数据（eg.不用计数）

- 2.属性方法：把实例方法伪装成属性，调用时无需括号

  - ```python
    class Student:
        def __init__(self, name, score):
            self.name = name
            self.__score = score  # 私有属性
        
        @property
        def score(self):
            return self.__score  # 读取属性
        
        @score.setter
        def score(self, new_score):
            if 0 <= new_score <= 100:
                self.__score = new_score
            else:
                raise ValueError("分数必须在0-100之间")
    
    # 调用
    s = Student("小明", 90)
    print(s.score)       # 读取（无括号）
    s.score = 85         # 修改
    # s.score = 105      # 报错：ValueError
    ```

### 4.私有变量和私有办法

- 私有变量：以双下划线开头，python会对其名称进行改写，外部无法直接访问，确保数据安全

- 示例：

  ```python
  # 示例1
   def __init__(self):
          # 私有属性：面积
          self.__area = None
          # 每次创建实例时计数加1
          Shape.shape_count += 1
  # 示例2
       def get_area(self):
          """公开方法：获取面积"""
          if self.__area is None:  # 私有属性（变量）
              self.__area = self._calc_area()
          return self.__area
  ```

- 私有方法：以双下划线开头是python规定，仅在内部被调用，以单下划线开头是约定俗成，外部可以调用

- 示例：

  ```python
  def _calc_area(self):
          """计算面积的私有方法（需要子类重写）"""
          raise NotImplementedError("子类必须实现此方法")
  ```

### 5.封装

- 核心思想：对内隐藏细节，对外暴露接口，保证数据安全

- 实现方式：

| 写法        | 类型 | 访问限制                     | 示例                                 |
| ----------- | ---- | ---------------------------- | ------------------------------------ |
| __属性/方法 | 私有 | 外部无法直接访问，仅内部可用 | `self.__area`（私有面积属性）        |
| _属性/方法  | 保护 | 约定仅内部可用               | `_calc_area()`（保护的面积计算方法） |
| 无下划线    | 共有 | 外部可自由访问               | `get_area()`（公开的面积获取方法）   |

- 示例：

  ```python
  class Shape:
      def __init__(self):
          self.__area = None  # 私有属性：隐藏面积数据
      
      def get_area(self):  # 公开接口：安全访问面积
          if self.__area is None:
              self.__area = self._calc_area()
          return self.__area
  ```

- 核心作用：防止外部修改核心数据和简化外部使用

### 6.继承

- 核心思想：子类复用父类的属性和方法，同时可以有自己的特有功能，减少代码冗余

- 实现方式

  - 定义子类时指定父类：class 子类（父类）

  - 子类通过super（）调用父类办法，保证父类初始化逻辑进行

  - 示例：

    ```python
    class Circle(Shape):  # 定义子类时指定父类
        """圆形类"""
        
        def __init__(self, radius):
            super().__init__()  # 调用父类__init__,执行count累加，__area初始化
            # 实例变量：存储圆形的尺寸（半径）
            self.radius = radius  # 子类拓展属性
        
        def _calc_area(self):
            """重写面积计算逻辑（多态体现）"""
            return math.pi * self.radius ** 2
        
        def __str__(self):
            return f"圆形(半径={self.radius}, 面积={self.get_area():.2f})"
    ```

- 核心要点：
  - super():python内置函数，自动找到父类，调用父类办法
  - 子类可以重写父类方法，实现个性化逻辑
  - 类方法适配继承：cls参数自动指向调用的类（父/子），比静态方法灵活

### 7.多态

- 核心思想：不同子类对同一父类方法的重写，为子类所特有，使得同一方法调用在不同示例上表现出不同行为，比如，父类设定异常情况，子类直接编写

- 实现方法：

  - 父类定义统一接口，子类重写该接口实现特有逻辑
  - 调用时无需区分实例类型，直接调用统一方法

- 示例：

  ```python
   def _calc_area(self):
          """计算面积的私有方法（需要子类重写）"""
          raise NotImplementedError("子类必须实现此方法")
          
    def _calc_area(self):
          """重写面积计算逻辑（多态体现）"""
          return math.pi * self.radius ** 2
  ```

- 核心作用：

  - 代码更加灵活：新增子类，无需遍历/调用逻辑 
  - 符合新增子类，无需改原有调用代码的开闭原则

### 8.补充

- str.strip()

  - 默认参数：strip()方法默认参数是None

  - 隐含行为：当参数为None或未提供，会删除字符串开头和结尾空白符（空格，制表符\t，换行符\n，回车符\r，换页符\f）

  - 不仅删除空格，还删除其他空白字符

  - 如果只要删除空格，需要显示传递参数’ ‘

  - 示例：

  - ```python
    # 测试 str.strip() 的不同行为
    test_string = "  \t\n  Hello World  \r\n  "
    
    print("原始字符串:", repr(test_string))
    print("默认strip():", repr(test_string.strip()))
    print("只删除空格:", repr(test_string.strip(' ')))
    print("删除特定字符:", repr(test_string.strip(' \n\t\rH')))
    ```

  - 结论：str.strip()的默认行为是删除字符串两端的所有空白字符（空格，制表符等），而不仅仅是空格。如果只需要删除空格，应添加特定的参数，删除特定字符也是一样，需要添加特定的参数
