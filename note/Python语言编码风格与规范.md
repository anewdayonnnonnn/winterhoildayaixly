# Python语言编码风格与规范

#### 1.1缩进风格

- 对于每级缩进。使用4个空格键，不能混用tab键（不同编辑器tab长度不一）

- 续行需要垂直对齐  `如函数参数悬挂`

  ```
  # 正确示范
  
  # 与定界（括号）符对齐
  foo = long_function_name(var_one, var_two,
                           var_three, var_four)
  
  # 换行并增加4个额外的空格（一级缩进）
  def long_function_name(
          var_one, var_two, var_three,
          var_four):
      print(var_one)
  
  # 悬挂需要增加一级缩进
  foo = long_function_name(
      var_one, var_two,
      var_three, var_four)
  ```

  ```
  # 错误示范
  
  # 当不使用垂直对齐时，第一行不允许加参数
  foo = long_function_name(var_one, var_two,
      var_three, var_four)
  
  # 没有区分函数参数和函数体
  def long_function_name(
      var_one, var_two, var_three,
      var_four):
      print(var_one)
  ```

- 如果包含定界符（三种括号）跨越多行，定界符的括回符另起一行顶格对齐或对齐第一个非空字符，`对函数参数和列表等均适用`

```
# 正确示范
# 另起一行顶格
my_list = [
    1, 2, 3,
    4, 5, 6,
]
# 对齐第一个非空字符  
my_list = [
    1, 2, 3,
    4, 5, 6,
    ]    
```

#### 1.2每行最大长度

- 每行最多不超过120个字符，过多字符会导致阅读障碍，使得缩进失效 ；如果需要长字符串，可以括号隐形连接或使用续行符\
- 例外：1.导入模块语句 2.注释中包含的URL（网址）

```
# 允许：导入语句即使超长，也无需拆分（除非特别极端）
from my_project.utils.data_processing.user_behavior_analysis import
(get_user_click_data, get_user_purchase_data, get_user_browse_duration)
# 允许：注释里的URL即使超长，无需拆分（URL拆分会失效）
# 参考文档：https://docs.python.org/3/library/stdtypes.html#str.splitlines
def split_text(text):
    return text.splitlines()
```

#### 1.3空白符

- 在表达式赋值符号，操作符号左右至少一个空格
- 注释每一行以#和空格起手

```
# 正确示范
x = y + 1
# 错误示范
x = y+1
x=y+1
```

- 写完一个类、一个函数，或者一段独立功能的代码后，空一行分隔，让代码块之间有清晰的视觉边界，避免所有代码挤在一起

```
def func1():
    print("函数1")

# 函数1结束后空一行
def func2():
    print("函数2")

# 函数2结束后空一行
class MyClass:
    def method(self):
        print("方法")
        
        # 一段完整功能代码后空一行
        a = 1 + 2
        b = a * 3
        print(b)
        
        # 空行分隔不同功能代码
        c = b - 1
        print(c)
```



- 禁止代码/注释行尾多余的空格/tab键，减少源码管理系统协作麻烦

#### 1.4二目操作符

- 操作符允许在**换行后**再出现

```
# 正确示范
# 易于将运算符与操作数匹配，可读性高
income = (gross_wages
          + taxable_interest
          + (dividends - qualified_dividends)
          - ira_deduction
          - student_loan_interest)
```

#### 1.5源文件编码

- 源文件编码需统一使用 `UTF-8` 编码，以下内容需要增加到每一个 python 文件的头部。

```
# -*- coding: utf-8 -*-
```

- 换行符一致使用LF（\n)

#### 1.6模块引用

- 每个导入占一行，最好按标准库，拓展库，自定义库的顺序依次导入

```
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
```

#### 1.7命名规范

- 避免单字符命名，除了计数器和迭代器
- 避免使用连字符-,用下划线_代替
- 避免双下划线开头与结尾的名称