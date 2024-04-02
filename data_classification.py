from collections import defaultdict
from datetime import datetime, time, timedelta

#센서 데이터 리스트를 사용자 ID별로 분류합니다.
def classify_data_by_id(sensor_data_list):
    data_by_id = defaultdict(list)
    for data in sensor_data_list:
        data_by_id[data[1]].append(data)
    return data_by_id

#데이터 포인트의 카테고리와 날짜를 결정합니다.
def get_custom_date_and_category(timestamp, sunrise_today_time, sunset_today_time, current_date):
    if sunrise_today_time <= timestamp < sunset_today_time:
        return current_date.strftime('%Y-%m-%d'), 'daytime'
    elif timestamp < sunrise_today_time:  # 새벽 시간 데이터 처리
        return (current_date - timedelta(days=1)).strftime('%Y-%m-%d'), 'sunset'
    else:
        return current_date.strftime('%Y-%m-%d'), 'sunset'
