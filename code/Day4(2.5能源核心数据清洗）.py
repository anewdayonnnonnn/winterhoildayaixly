import json
import re
import unicodedata

# 先清洗后过滤，因为有些非数字的字符串，列表等可能是有效数据
def get_data(s):  # 从字符串提取数字，返回浮点数或None
    if s is None:
        return None

    # 将元素都转化为字符串
    if not isinstance(s, str):
        s = str(s)

    # 手动映射处理全角数字
    s = s.translate(str.maketrans('０１２３４５６７８９．', '0123456789.'))
    # 全局标准化，去除其他异常字符
    s = unicodedata.normalize("NFKC", s.strip())

    # 跳过空字符串和纯空白元素
    if not s or s.isspace():
        return None

    # 用字典归档特殊字符，处理特殊字符
    special_str = {
        "null": None,"undefined": None,"nan": None,
        "infinity": float("inf"),"-infinity": float("-inf"),
        "true": 1.0,"false": 0.0
    }
    if s.lower() in special_str:  # 全部归档为小写字母
        return special_str[s.lower()]

    # 利用正则化移除干扰字符 提取数字
    cleaned = re.sub(r'[^\d\.eE\+\-]','',s)

    # 处理无数字字符元素
    if not cleaned:
        match = re.search(r'[\d\.]+',s)
        if match:
            cleaned = match.group()
        else :
            return None

    # 转换提取数字并且检验（NaN和无穷）
    try :
        num = float(cleaned)
        if num != num or abs(num) == float("inf"):
            return None
        return num
    except (ValueError, TypeError):
        if ',' in s:
            s_without_commas = s.replace(',', '')
            try :
                num = float(s_without_commas)
                if num != num or abs(num) == float("inf"):
                    return None
                return num
            except (ValueError, TypeError):
                return None
        return None
# c处理列表，字典等元素
def process_list_data(item, results):
    if isinstance(item, list):
        for sub_item in item:
            process_list_data(sub_item, results)
    elif isinstance(item, dict):
        for value in item.values():
            process_list_data(value, results)
    else :
        num = get_data(item)
        # 过滤有效数字并且归一化
        if num is not None and num >= 80:
            nor_num = num / 100
            status = "核心过载" if nor_num > 1.0 else "运转正常"

            results.append({
                "original": item,
                "value": round(num, 4),
                "normalized": round(nor_num, 4),
                "status": status
            })

def clean_data(data_list):  # 清洗数据 返回归一化结果
    results = []  # 存储归一化结果

    # 遍历列表 清洗数据提取数字
    process_list_data(data_list, results)
    return results

if __name__ == "__main__":
    # 导入数据
    with open("../data/energy_data.json", "r", encoding="utf-8") as f:
        raw_data = json.load(f)
    # 调用清洗函数
    end_data = clean_data(raw_data)
    print(end_data)

