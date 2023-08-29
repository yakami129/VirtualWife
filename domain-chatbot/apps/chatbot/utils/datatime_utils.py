from datetime import datetime


def get_current_time_str() -> str:
    """获取当前时间"""
    # 获取当前时间
    current_time = datetime.now()
    # 将时间格式化为指定格式
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_time
