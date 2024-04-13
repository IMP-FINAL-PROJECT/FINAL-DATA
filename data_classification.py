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

def add_gps_data_with_timestamps(data, summary, custom_date):
    # GPS 데이터와 시간 인덱스를 가져옵니다.
    gps_data_list = eval(data[field_mappings.SENSOR_GPS_INDEX])
    hour_of_day = data[field_mappings.SENSOR_HOUR_INDEX]
    date = data[field_mappings.SENSOR_TIMESTAMP_INDEX]
    
    # 날짜와 시간을 결합하여 datetime 객체를 생성합니다.
    date_time = datetime.combine(date, time(hour=hour_of_day))
    
    # GPS 데이터를 처리하고 타임스탬프를 추가합니다.
    accumulated_duration = 0  # 누적 시간 초기화
    for gps_point in gps_data_list:
        latitude, longitude, duration_ms = gps_point
        duration_seconds = duration_ms / 1000  # 밀리초를 초로 변환
        timestamp = date_time + timedelta(seconds=accumulated_duration)  # 누적 시간을 기반으로 타임스탬프 계산
        accumulated_duration += duration_seconds  # 누적 시간 업데이트
        formatted_gps_point = [latitude, longitude, duration_ms, timestamp.isoformat()]
        
        # summary 객체에 처리된 GPS 데이터를 추가합니다.
        summary[custom_date]['gps']['gps'].append(formatted_gps_point)


#개별 데이터 합산 및 처리 함수 
def process_data_point(data, summary, custom_date, category):
    illuminance_array = eval(data[field_mappings.SENSOR_ILLUMINANCE_INDEX])
    avg_illuminance = sum(illuminance_array) / len(illuminance_array) if illuminance_array else 0
    gps_data_list = eval(data[field_mappings.SENSOR_GPS_INDEX])

    summary[custom_date][category]['count'] += 1
    #summary[custom_date]['gps']['gps'].extend(gps_data_list)
    add_gps_data_with_timestamps(data, summary, custom_date)
    summary[custom_date]['gps']['confirm'].append(data[field_mappings.SENSOR_HOUR_INDEX])
    summary[custom_date][category]['pedometer'] += data[field_mappings.SENSOR_PEDOMETER_INDEX]
    summary[custom_date][category]['screen_frequency'] += data[field_mappings.SENSOR_SCREEN_FREQUENCY_INDEX]
    summary[custom_date][category]['screen_duration'] += data[field_mappings.SENSOR_SCREEN_DURATION_INDEX]
    if sum(illuminance_array) > 0:
        summary[custom_date][category]['illuminance_sum'] += avg_illuminance


