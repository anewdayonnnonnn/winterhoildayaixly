# 用一行代码（推导式）生成 1 到 10 的平方数列表
result = [i * i for i in range(1,11)]
print(result)

# 用 map 结合 lambda 给全班同学的名字加上统一前缀
name = ["张三", "李四", "王五", "赵六"]
print(list(map(lambda x : "QG_" + x, name)))

