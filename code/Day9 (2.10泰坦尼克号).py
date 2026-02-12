import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 读取文件
df = pd.read_csv("../data/Titanic.csv",encoding="utf-8")

# 查看基本信息
df.info()

# 数据清洗
df.drop(["Cabin"],axis=1,inplace=True)  # 先删除缺失较多的数据

numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns  # 数值类填充缺失值
df[numerical_cols] = df[numerical_cols].fillna(df[numerical_cols].mean())

not_numerical_cols = df.select_dtypes(exclude=['int64', 'float64']).columns  # 非数值类填充缺失值
df[not_numerical_cols] = df[not_numerical_cols].fillna("未知")

duplicate_count = df.duplicated().sum()  # 去除重复值
if duplicate_count > 0:
    df = df.drop_duplicates()

# 分析各项指标生还率
plt.figure(figsize=(16,10))  # 创建画布，存放子图
# 1.Pclass舱位等级
plt.subplot(2,4,1)
sns.countplot(x='Pclass', hue='Survived',data=df)
plt.title("Pclass and Survived")

# 2.Sex性别
plt.subplot(2,4,2)
sns.countplot(x='Sex', hue='Survived',data=df)
plt.title("Sex and Survived")

# 3.Age年龄
plt.subplot(2,4,3)
sns.histplot(x='Age', hue='Survived',kde=True,data=df,bins=30)
plt.title("Age and Survived")

# 4.SibSp配偶/兄弟姐妹数量
plt.subplot(2,4,4)
sns.barplot(x='SibSp', y='Survived',data=df)
plt.title("SibSp and Survived")

# 5.Parch父母/子女数量
plt.subplot(2,4,5)
sns.barplot(x='Parch', y='Survived',data=df)
plt.title("Parch and Survived")

# 6.Fare船票价格
plt.subplot(2,4,6)
sns.boxplot(x='Survived', y='Fare',data=df)
plt.title("Fare and Survived")

# 7.Embarked登船港口
plt.subplot(2,4,7)
sns.countplot(x='Embarked', hue='Survived',data=df)
plt.title("Embarked and Survived")

# 8.总体生存率
plt.subplot(2,4,8)
survived_rate  = df['Survived'].mean()
sns.countplot(x='Survived',data=df)
plt.title("Survived Rate")

# 显示
plt.tight_layout()
plt.show()
print(f"生还率{survived_rate:.2%}")

"""
1.Pclass 舱位等级越高存活率越高，一分钱一分货
2.Sex 女性生存率更高，妇女优先
3.Age 低年龄存活率更搞，儿童优先
4，SibSp 带配偶/兄弟姐妹数量少存活率较高
5.Parch 带父母/子女数量少存活率较高
6，Fare 生还者大多低价票，但也有极端值
7.在S港口上船最多，死亡最多，生存率和q港口差不多，c港口生存率较高
8.总生存率为38.38%，事故伤亡惨重
"""