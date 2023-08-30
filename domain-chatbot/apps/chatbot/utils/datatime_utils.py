import datetime
import pytz

def get_current_time_str():
  current_time = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
  formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
  return formatted_time
