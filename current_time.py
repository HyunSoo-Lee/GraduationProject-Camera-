from datetime import datetime
from pytz import timezone
import db_connect as db

def korea_time():
    # 한국 시간대 설정
    korea_timezone = timezone('Asia/Seoul')

    # 현재 시간 가져오기
    korea_current_time = datetime.now(korea_timezone)

    return korea_current_time

def format_datetime(datetime_value):
    # 원하는 형식으로 포맷팅
    formatted_datetime = datetime_value.strftime('%Y-%m-%d %H:%M:%S')

    return formatted_datetime

def get_time():
    korea_current_time = korea_time()
    formatted_time = format_datetime(korea_current_time)
    time = "'" + formatted_time + "'"
    return time
