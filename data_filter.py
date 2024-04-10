from excel_data_loader import get_sunrise_sunset, round_up_time
from datetime import datetime, timedelta, time

# 데이터베이스에 이미 존재하는 항목 필터링
def filter_existing_entries(sensor_data_list, existing_combinations):
    existing_entries_set = set()

    # sensor_data_list 순회
    for data in sensor_data_list:
        id = data[1]  # 'id'는 각 튜플의 두 번째 요소로 가정
        date = data[-2]  # 'date'는 각 튜플의 끝에서 두 번째 요소로 가정
        hour = data[-1]

        # 날짜 조정 로직
        sunrise_today, _ = get_sunrise_sunset(date.strftime('%m%d'))
        rounded_sunrise_today = round_up_time(sunrise_today)
        sunrise_today_time = datetime.combine(date, time(rounded_sunrise_today, 0))
        adjusted_date = adjust_date_by_hour(date, hour, sunrise_today_time)

        # id와 조정된 date 조합이 데이터베이스에 존재하고, 중복이 아닌 경우에만 저장
        entry = (id, str(adjusted_date))
        if entry in existing_combinations and entry not in existing_entries_set:
            existing_entries_set.add(entry)

    # 순서가 중요하지 않다면, 집합을 직접 반환할 수 있음
    return list(existing_entries_set)

    # 순서를 유지해야 한다면, 집합을 리스트로 변환하여 반환
    # return list(existing_entries_set)

    # round_up_time, get_sunrise_sunset 함수가 이미 정의되어 있다고 가정합니다.

def adjust_date_by_hour(date, hour, sunrise_today):
    # date와 hour를 datetime 객체로 결합
    current_datetime = datetime.combine(date, time(hour, 0))
    
    # 0시부터 5시 사이이거나 (6시부터 8시 사이이면서 sunrise_today보다 hour가 작은 경우)
    if current_datetime.hour < 6 or (6 <= current_datetime.hour <= 8 and current_datetime < sunrise_today):
        # 날짜를 하루 빼줌
        adjusted_date = current_datetime - timedelta(days=1)
    else:
        # 그 외의 경우에는 날짜를 변경하지 않음
        adjusted_date = current_datetime
    
    return adjusted_date.date()
