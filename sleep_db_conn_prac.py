from datetime import datetime
from pytz import timezone

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

startt = []
endt = []

i = 0

korea_current_time = get_korea_current_time()
formatted_time = format_datetime(korea_current_time)
print(formatted_time)

while True:
    i = input()
    if i == '10':
        korea_current_time = get_korea_current_time()
        formatted_time = format_datetime(korea_current_time)
        if not startt:
            startt.append(formatted_time)
        else:
            startt.clear()
            startt.append(formatted_time)
    print(startt)

