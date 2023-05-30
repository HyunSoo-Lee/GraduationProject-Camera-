import db_connect as db
from datetime import datetime
from pytz import timezone

#기본적인 row return
user_val = db.find_row('user', 'user_id', '2')
print(user_val)
print(user_val[0])
print("/////////////////")

#user id 가져오기
id = db.find_id('user', 'nickname', 'JHM')
print(id)
print("/////////////////")

def get_korea_current_time():
    # 한국 시간대 설정
    korea_timezone = timezone('Asia/Seoul')

    # 현재 시간 가져오기
    korea_current_time = datetime.now(korea_timezone)

    return korea_current_time

def format_datetime(datetime_value):
    # 원하는 형식으로 포맷팅
    formatted_datetime = datetime_value.strftime('%Y-%m-%dT%H:%M:%S')

    return formatted_datetime

# 한국의 현재 시간을 가져옴
korea_current_time = get_korea_current_time()

# 원하는 형식으로 포맷팅
formatted_time = format_datetime(korea_current_time)

print(formatted_time)
time = '\'' + formatted_time + '\''
print(time)
db.edit_val(id, 'sleep_time', 'endt', time)
new_sleep_val = db.find_row('sleep_time', 'user_id', id)

db.sleep_ins(1, time,time, 0)
