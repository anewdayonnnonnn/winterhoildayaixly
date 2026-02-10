import pandas as pd

# 读取文件
df = pd.read_csv("../data/housecost.csv",encoding="utf-8")

# 数据清理
# =====1.查看基本信息=====
df.info()

# =====2.填补缺失值=====
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

not_numeric = df.select_dtypes(exclude=['int64','float64']).columns
df[not_numeric] = df[not_numeric].fillna("未知")

# =====3.处理重复值=====
duplicate_count = df.duplicated().sum()
if duplicate_count > 0:
    df = df.drop_duplicates()

