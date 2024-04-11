from collections import defaultdict
from datetime import datetime, time, timedelta
import field_mappings
#센서 데이터 리스트를 사용자 ID별로 분류합니다.
def classify_data_by_id(sensor_data_list):
    data_by_id = defaultdict(list)
    for data in sensor_data_list:
        data_by_id[data[field_mappings.SENSOR_ID_INDEX]].append(data)
    return data_by_id

#데이터 포인트의 카테고리와 날짜를 결정합니다.
def get_custom_date_and_category(timestamp, sunrise_today_time, sunset_today_time, current_date):
    if sunrise_today_time <= timestamp < sunset_today_time:
        return current_date.strftime('%Y-%m-%d'), 'daytime'
    elif timestamp < sunrise_today_time:  # 새벽 시간 데이터 처리
        return (current_date - timedelta(days=1)).strftime('%Y-%m-%d'), 'sunset'
    else:
        return current_date.strftime('%Y-%m-%d'), 'sunset'

#개별 데이터 합산 및 처리 함수 
def process_data_point(data, summary, custom_date, category):
    illuminance_array = eval(data[field_mappings.SENSOR_ILLUMINANCE_INDEX])
    avg_illuminance = sum(illuminance_array) / len(illuminance_array) if illuminance_array else 0
    gps_data_list = eval(data[field_mappings.SENSOR_GPS_INDEX])

    summary[custom_date][category]['count'] += 1
    summary[custom_date]['gps']['gps'].extend(gps_data_list)
    summary[custom_date]['gps']['confirm'].append(data[field_mappings.SENSOR_HOUR_INDEX])
    summary[custom_date][category]['pedometer'] += data[field_mappings.SENSOR_PEDOMETER_INDEX]
    summary[custom_date][category]['screen_frequency'] += data[field_mappings.SENSOR_SCREEN_FREQUENCY_INDEX]
    summary[custom_date][category]['screen_duration'] += data[field_mappings.SENSOR_SCREEN_DURATION_INDEX]
    if sum(illuminance_array) > 0:
        summary[custom_date][category]['illuminance_sum'] += avg_illuminance
