import re


def remove_emojis(input_string) -> str:
    # 使用正则表达式删除所有表情符号
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # 表情符号
                               u"\U0001F300-\U0001F5FF"  # 符号与杂项符号
                               u"\U0001F680-\U0001F6FF"  # 交通和地图符号
                               u"\U0001F700-\U0001F77F"  # 国际音标扩展符号
                               u"\U0001F780-\U0001F7FF"  # 表情符号补充
                               u"\U0001F800-\U0001F8FF"  # 语言补充
                               u"\U0001F900-\U0001F9FF"  # 符号与象形文字补充
                               u"\U0001FA00-\U0001FA6F"  # 扑克牌
                               u"\U0001FA70-\U0001FAFF"  # 旗帜（Emoji表情）
                               u"\U0001F004"  # 单个符号-标签
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', input_string)


def remove_spaces_and_tabs(input_string) -> str:
    text = input_string.replace(" ", "").replace("\t", "")
    return text

def remove_special_characters(input_string) -> str:
    # 定义正则表达式模式，匹配特殊符号，同时保留 .．！？~、,
    pattern = r'[^\w\s.．！？~、,，。]'  # 这个模式匹配除了字母、数字、空格和指定符号之外的所有字符

    # 使用 re.sub() 函数删除匹配的特殊字符
    cleaned_string = re.sub(pattern, '', input_string)

    return cleaned_string
