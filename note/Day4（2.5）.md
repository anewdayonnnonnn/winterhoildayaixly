# Day4（2.5）

### 1.流程控制+异常捕获

- **分支判断**：if-elif-else结构，用于根据条件执行不同代码块
- **循环结构**：
  - `for循环`:用于遍历可迭代对象（如列表、字符串）
  - `while循环`:用于条件满足时重复执行代码
- **异常捕获**：`try-expect` 机制，捕获并处理程序运行时的错误，避免程序崩溃

> 异常就是**程序运行过程中出现的意外错误**，它会中断代码的正常执行流程，如果不处理，程序会直接崩溃并抛出错误信息

### 2.推导式＋函数式编程

- **列表推导式**：简洁生成列表的语法

  - ```
    [x for x in range(10) if x % 2 == 0]
    
    # 例子
    result = [i * i for i in range(1,11)]
    ```

-  **匿名函数**：`lambda` 表达式，用于定义简单的一次性函数

  - ```
    lambda x: x * 2
    
    # 例子
    name = ["张三", "李四", "王五", "赵六"]
    print(list(map(lambda x : "QG_" + x, name)))
    ```

- **高阶函数**：

  - `map`：将函数作用于可迭代对象的每个元素，返回新的迭代器

  - `filter`：根据函数的布尔结果过滤可迭代对象的元素

  - ```
    add_ten = lambda x: x * 2
    print(list(map(add_ten,[1,2,3,4,5])))
    is_even = lambda x:x % 2 == 0
    print(list(filter(is_even, [1,2,3,4,5])))
    ```

### 3.其他

- **JSON（JavaScript Object Notation）** 是一种**轻量级、纯文本格式**的数据交换文件，后缀名为 `.json`，专门用于存储和传输结构化数据，是编程中最常用的配置文件、数据存储格式之一

- **with open()**:Python 中**用于读写文件的标准、最推荐写法**，核心作用是安全、简洁地打开文件，完成读写操作后**自动关闭文件**

  - ```
    # 通用格式
    with open(文件路径, 打开模式, encoding=编码格式) as 文件对象:
        # 缩进代码块内执行文件读写操作
        操作语句
        
    with open("../data/energy_data.json", "r", encoding="utf-8") as f:
        raw_data = json.load(f)    
    ```

- **isinstance（）**：python内置函数，**用于判断一个对象的类型是否属于指定的数据类型 / 类**，返回布尔值（`True`/`False`）

  - ```
    isinstance（要检查的对象，类型参数）
    # 字符串判断
    print(isinstance("hello", str))   # True
    print(isinstance(123, str))       # False
    
    # 数字判断（int/float）
    print(isinstance(100, int))       # True
    print(isinstance(99.9, float))    # True
    
    # 列表/字典判断
    print(isinstance([1,2], list))    # True
    print(isinstance({"a":1}, dict))  # True
    
    # 判断是否为 整数 或 浮点数
    num = 88.8
    print(isinstance(num, (int, float)))  # True
    
    # 判断是否为 列表 或 字典
    data = []
    print(isinstance(data, (list, dict))) # True
    ```

- **re**：Python **内置的正则表达式模块**，全称为 **Regular Expression**（正则表达式），专门用于**字符串的匹配、查找、替换、分割**等文本处理操作，也是你数据清洗代码里的核心工具，用来过滤干扰字符、提取数字

  - `*re.sub(pattern, repl, string)*`： **字符串替换/删除**

  - ```
    # 按照正则规则匹配内容，并用指定字符替换，是你清洗干扰字符的核心方法
    # pattern： 正则匹配规则
    # repl： 替换后的字符
    # string： 待处理的字符串
    
    cleaned = re.sub(r'[^\d\.eE\+\-]','',s)
    ```

  - *`re.search(pattern, string)*`:扫描整个字符串，**返回第一个匹配成功的对象**，无匹配则返回`None`

  - ```
    match = re.search(r'[\d\.]+',s)
    ```

  - `*match.group()*`:配合`re.search`/`re.match`使用，**提取匹配到的具体文本内容**。

  - ```
    if match:
        cleaned = match.group()
    ```

  - | 符号     | 含义                                            | 代码中应用                          |
    | -------- | ----------------------------------------------- | ----------------------------------- |
    | r' '     | 原始字符串标记，防止反斜杠`\`被 Python 转义     | 所有正则规则前缀，固定写法          |
    | []       | 字符集，匹配括号内**任意一个字符**              | `[\d\.eE]` 匹配数字 / 小数点 /e/E   |
    | ^        | 放在`[]`开头：**取反匹配**                      | `[^\d...]` 匹配「非指定字符」       |
    | \d       | 匹配所有阿拉伯数字（0-9）                       | 提取数字核心规则                    |
    | \.       | 匹配字面量小数点（`.`在正则中是通配符，需转义） | 适配小数格式                        |
    | +        | 量词，匹配**1 次及以上**连续字符                | `[\d\.]+` 匹配连续数字 / 小数点组合 |
    | eE\\+\\- | 匹配科学计数法符号、正负号                      | 支持`1e2`、`-80`、`+90`格式         |

- if __name__ == "__main__":判断当前脚本是否被直接运行，若是则执行代码块内的逻辑，被导入时则不执行。

  - ```
    # 这是你的主程序入口判断
    if __name__ == "__main__":
        # 读取数据、调用清洗函数、打印结果
        with open("../data/energy_data.json", "r", encoding="utf-8") as f:
            raw_data = json.load(f)
        end_data = clean_data(raw_data)
        print(end_data)
    ```

- **unicodedata**:Python **内置的标准库**，专门用于处理 **Unicode 字符**的标准化、属性查询、字符分类等操作

  - ```
    unicodedata.normalize(form, unistr)
    # form 标准化格式 选NFKC最适合数据清洗
    # unistr 需要标准化的Unicode字符串 
    
    # 先手动映射全角数字/小数点，再做全局Unicode标准化
    s = s.translate(str.maketrans('０１２３４５６７８９．', '0123456789.'))
    # 全局标准化，统一字符格式
    s = unicodedata.normalize("NFKC", s.strip())
    ```

    