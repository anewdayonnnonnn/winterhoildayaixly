# Pandas库学习（Day8  2.9）

pandas是python数据分析中非常重要的库，它利用数据框和数据表让数据处理和操作变得简单，同时，在数据预处理，填补缺失值，时间序列处理和数据可视化方面均有应用

## 基础前置知识

- **Series（一维序列）**

  - ```
    # 生成一个序列
    s1 = pd.Series(data = [1, 2, 3, 4],index = ["b","c","d","e"],name = "var1")
    print("数值："，s1.values)  # 获取序列的数值
    print("索引："，s1.index)  # 获取序列的索引
    
    # 也可以通过字典生成序列
    s2 = pd.Series({"A":100,"B":200,"C":300,"D":400})
    print(s2.value_counts())  # 计算序列中每个取值出现的次数
    ```

- **DataFrame(二维表格)**：一行表格就是一个序列

  - ```
    # 通过数组生成数据表
    data = np.arange(32).reshape(4,8)
    df1 = pd.DataFrame(data = data,
                       columns = ["A","B","C","D","E","F","G","H"],
                       index = ["a","b","c","d"])
    # 将字典生成数据表
    data = { “name":["huonan","yelu","mudie","jett","baoan"],
             "age" :[10,15,10,13,12],
             "sex":["F","F","M","M","F"]}
    df2 = pd.DataFrame(data=data)
    df2["high"]=[170,176,164,170,180]  # 为表格添加新的变量
    df2["Weight"]=[50,50,50,50,50]
    ```

- **查看数据的基本方法**

  - head（）----看前几行（默认前5行）

  - ```
    df1.head()  # 前5行
    df1.head(3)  # 前3行 
    ```

  - tail（）---看最后几行（默认最后5行）

  - ```
    df2.tail()  # 后5行
    df2.tail(2)  # 后2行
    ```

  - ==**info（）**==---查看行数，列数，字段类型，是否有缺失值，内存占用，数据分析第一句

  - ```
    df1.info()
    # =======输出内容======
    # 总行数，总列数
    # 每列排名，数据类型（int/float/object)
    # 非空值数量
    # 整体内存大小
    ```

  - describe() ---看统计描述（自动计算均值，标准差，最小/最大值，分位数，中位数） 

  - ```
    df1.describe()
    ```

  - shape---看形状（行数，列数）

  - ```
    df1.shape()  # 输出（行数，列数）
    ```

  - columns ---看所有列名

  - ```
    df1.columns
    ```

  - dtypes---看每列的数据类型

  - ```
    df1.dtypes
    ```

## 数据读取与写入

#### 核心逻辑:pandas读取文件，转为dataframe，处理后，导出为指定格式

- 读取csv文件 ----pd.read_csv()

  - ```
    import pandas as pd
    # 基本读取
    df = pd.read_csv("data.csv",encoding="utf-8")
    # 指定读取
    # sep 分隔符  header 哪一行为列名 uescols 指定读取的列 
    df = pd.read_csv("data.csv",sep=";",header=0,usecols=["name","age"])
    ```

- 读取excel文件 ---pd.read_excel()

  - ```
    # 基本读取
    df = pd.read_excel("data.xlsx",sheet_name=0)
    
    # 指定读取
    # sheet_name 要读取的工作表名称 header 列名所在行 usecols 指定读取的列
    df = pd.read_excel("data.xlsx",sheet_name="Sheet2")
    ```

- 读取txt/文本文件：---pd.read_csv 适配分隔符读取

  - ```
    df = pd.read_csv("data.txt",sep="\t",encoding="utf-8")
    df = pd.read_csv(“data.txt",sep="\s+")
    ```

- 读取json文件：---pd.read_json

  - ```
    df = pd.read_json("data.json")
    ```

- 数据导出保存  ---to_csv(),to_excel()

  - ```
    # 保存为csv报表
    df.to_csv("output.csv",index=False,encoding="utf-8")  # 加index=False避免多余索引
    
    # 保存为excel文件
    df.to_excel("output.xlsx",sheet_name="Sheet1"，index=False)  # 加index=False避免多余索引
    ```

## 简单数据清洗

1.缺失值处理

先统计缺失值，再决定删还是填

- 查看缺失值

  - ```
    import pandas as pd
    df = pd.read_csv("data.csv")
    
    # 查看每个单元格是否缺失
    df.isnull()
    # 统计每列缺失数量
    df.isnull().sum()
    # 统计总缺失数量
    df.isnull().sum().sum()
    ```

- 删除缺失值

  - ```
    # 删除任何含有缺失值的行
    df.dropna()
    # 删除所有值都缺失的行
    df.dropna(how="all")
    # 只保留至少有5个非缺失值的行
    df.dropna(thresh=5)
    # 按列删除
    df.dropna(axis=1)
    ```

- 填充缺失值

  - ```
    # 用常数0填充
    df.fillna(0)
    # 用列均值填充
    df.fillna(df.mean())
    # 用列中位数填充
    df.fillna(df.median())
    # 用前一个有效值填充（向前填充）
    df.fillna(method="ffill")
    ```

2.重复值处理

重复行会影响统计结果，先识别再去重

- 查找重复行

  - ```
    # 返回布尔值，标记重复行
    df.duplicated()
    # 统计重复行数
    df.duplicated().sum()
    # 查看具体的重复行
    df[df.duplicated()]
    ```

- 删除重复行

  - ```
    # 删除所有完全重复的行
    df.drop_duplicates()
    # 只根据指定列去重（如根据'姓名'和'身份证号'）
    df.drop_duplicates(subset=["姓名", "身份证号"])
    # 保留最后一次出现的重复行
    df.drop_duplicates(keep="last")
    ```

3.数据格式与异常值处理

使得数据更加规整

- 数据类型转换

  - ```
    # 将'年龄'列从字符串转为整数
    df['年龄'] = df['年龄'].astype(int)
    # 将'日期'列转为日期类型
    df['日期'] = pd.to_datetime(df['日期'])
    ```

- 列名重命名

  - ```
    # 用rename方法
    df.rename(columns={'旧列名': '新列名'}, inplace=True)
    # 直接修改columns属性
    df.columns = ['列1', '列2', '列3']
    ```

- 提出无用行列

  - ```
    # 删除指定列
    df.drop(columns=['无用列1', '无用列2'], inplace=True)
    # 删除指定行（如索引为5的行）
    df.drop(index=5, inplace=True)
    ```

- 筛选有效数据

  - ```
    # 条件过滤：只保留年龄在18到60岁之间的数据
    df = df[(df['年龄'] >= 18) & (df['年龄'] <= 60)]
    # 剔除明显异常值，如消费金额为负数
    df = df[df['消费金额'] > 0]
    ```

4.基础数据规整

使得数据结构更加符合分析需求

- 行列选择后重置索引

  - ```
    # 按标签名取行和列
    df.loc[:, ['姓名', '年龄']]
    # 按位置索引取行和列
    df.iloc[:, [0, 1]]
    # 重置索引为1 2 3......，去掉旧索引
    df.reset_index(drop=True, inplace=True)
    ```

- 数据排序

  - ```
    # 按'年龄'列升序排列
    df.sort_values(by='年龄', ascending=True)
    # 按多列排序，先按'城市'升序，再按'消费'降序
    df.sort_values(by=['城市', '消费'], ascending=[True, False])
    ```

- 字符串简单清洗

  - ```
    # 去除字符串两端的空格
    df['姓名'] = df['姓名'].str.strip()
    # 字符串替换，把'男'替换成'M'
    df['性别'] = df['性别'].str.replace('男', 'M')
    # 字符串转大写
    df['城市'] = df['城市'].str.upper()
    ```

    





