import datetime
import os
import pytz

TIMEZONE = os.environ.get("TIMEZONE","Asia/Shanghai")

def get_current_time_str():
    current_time = datetime.datetime.now(pytz.timezone(TIMEZONE))
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_time
