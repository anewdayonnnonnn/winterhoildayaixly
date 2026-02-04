# 原始情报
raw_info = " Agent:007_Bond; Coords:(40,74); Items:gun,money,gun; Mission:2025-RESCUE-X "

# 1. 清洗数据中的空格
cleanspace_info = raw_info.replace(" ","")

# 2.拆分片段，方便操作
parts_info = cleanspace_info.split(';')

# 3.提取各部分信息
# 截取代号
agent = parts_info[0].split(':')[1]

# 元组提取坐标
location_str = parts_info[1].split(':')[1]
x, y = location_str[1:-1].split(',')
location = (int(x),int(y))

# 集合装备去重
items_str = parts_info[2].split(':')[1]
items_list = items_str.split(',')
items = list(set(items_list))

# 截取任务代号
mission = parts_info[3].split(':')[1]

# 4.归档到Dict（字典）中
true_info = {
    "Agent": agent,
    "Location": location,
    "Items": items,
    "Mission": mission
}

