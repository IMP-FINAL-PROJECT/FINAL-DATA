from collections import defaultdict
from datetime import datetime, time, timedelta
from excel_data_loader import get_sunrise_sunset, round_up_time  # 가정된 외부 함수 호출

def classify_data_by_id(sensor_data_list):
    data_by_id = defaultdict(list)
    for data in sensor_data_list:
        data_by_id[data[1]].append(data)
    return data_by_id

def get_custom_date_and_category(timestamp, sunrise_today_time, sunset_today_time, current_date):
    if sunrise_today_time <= timestamp < sunset_today_time:
        return current_date.strftime('%Y-%m-%d'), 'daytime'
    elif timestamp < sunrise_today_time:  # 새벽 시간 데이터 처리
        return (current_date - timedelta(days=1)).strftime('%Y-%m-%d'), 'sunset'
    else:
        return current_date.strftime('%Y-%m-%d'), 'sunset'

def process_data_point(data, summary, custom_date, category):
    illuminance_array = eval(data[2])
    avg_illuminance = sum(illuminance_array) / len(illuminance_array) if illuminance_array else 0
    gps_data_list = eval(data[6])

    summary[custom_date][category]['count'] += 1
    summary[custom_date]['gps']['gps'].extend(gps_data_list)
    summary[custom_date][category]['pedometer'] += data[3]
    summary[custom_date][category]['screen_frequency'] += data[4]
    summary[custom_date][category]['screen_duration'] += data[5]
    if sum(illuminance_array) > 0:
        summary[custom_date][category]['illuminance_sum'] += avg_illuminance

def calculate_averages(summary):
    for categories in summary.values():
        for category in ['daytime', 'sunset']:
            if categories[category]['count'] > 0:
                categories[category]['illuminance_avg'] = categories[category]['illuminance_sum'] / categories[category]['count']
                categories[category]['pedometer'] /= categories[category]['count']
                categories[category]['screen_frequency'] /= categories[category]['count']
                categories[category]['screen_duration'] /= categories[category]['count']
                del categories[category]['illuminance_sum']  # 중간 합산값 삭제

def classify_and_summarize_data(sensor_data_list):
    data_by_id = classify_data_by_id(sensor_data_list)
    summary = defaultdict(lambda: defaultdict(lambda: {
        'gps': {'count': 0, 'gps': []},
        'daytime': {'count': 0, 'illuminance_sum': 0, 'illuminance_avg': 0, 'pedometer': 0, 'screen_frequency': 0, 'screen_duration': 0},
        'sunset': {'count': 0, 'illuminance_sum': 0, 'illuminance_avg': 0, 'pedometer': 0, 'screen_frequency': 0, 'screen_duration': 0}
    }))

    for id, data_list in data_by_id.items():
        for data in data_list:
            current_date = data[7]
            sunrise_today, sunset_today = get_sunrise_sunset(current_date.strftime('%m%d'))
            if sunrise_today != "No data available for the given date." and sunset_today != "No data available for the given date.":
                rounded_sunrise_today = round_up_time(sunrise_today)
                rounded_sunset_today = round_up_time(sunset_today)
                sunrise_today_time = datetime.combine(current_date, time(rounded_sunrise_today, 0))
                sunset_today_time = datetime.combine(current_date, time(rounded_sunset_today, 0))
                
                timestamp = datetime.combine(data[7], time(data[8]))
                custom_date, category = get_custom_date_and_category(timestamp, sunrise_today_time, sunset_today_time, current_date)
                process_data_point(data, summary[id], custom_date, category)
                
        calculate_averages(summary[id])

    return summary


# 센서 데이터 리스트 예시
# sensor_data_list = [...]
import datacall
batch_sensor_data_start_num = datacall.get_latest_start_num()
sensor_data_list = datacall.get_sensor_data(batch_sensor_data_start_num)
# classify_and_summarize_data 함수 사용
summary_data = classify_and_summarize_data(sensor_data_list)

# 요약 데이터 출력
for id, dates in summary_data.items():
    for date, periods in dates.items():
        print(f"ID: {id}, Date: {date}, Daytime Count: {periods['daytime']}, Sunset Count: {periods['sunset']}, GPS: {periods['gps']}")
