from datetime import datetime, timedelta, time
from excel_data_loader import get_sunrise_sunset, round_up_time
from dataselect import query_existing_id_date_combinations


def fetch_data_for_sunrise_intervals(existing_entries_list, batch_sensor_data_start_num):
    data_to_fetch = []
    
    for id, date_str in existing_entries_list:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        # 해당 날짜와 다음 날짜의 일출 시간을 구합니다.
        sunrise_today, _ = get_sunrise_sunset(date.strftime('%m%d'))
        sunrise_next_day, _ = get_sunrise_sunset((date + timedelta(days=1)).strftime('%m%d'))

        # 일출 시간을 반올림합니다.
        rounded_sunrise_today = round_up_time(sunrise_today)
        rounded_sunrise_next_day = round_up_time(sunrise_next_day)

        # 필요한 데이터를 리스트에 추가합니다.
        data_to_fetch.append((id, rounded_sunrise_today, rounded_sunrise_next_day,date))

    # 데이터베이스에서 데이터를 조회합니다.
    return(fetch_data_from_db(data_to_fetch, batch_sensor_data_start_num))
