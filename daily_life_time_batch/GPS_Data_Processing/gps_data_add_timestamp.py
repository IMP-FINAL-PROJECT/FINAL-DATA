from .gps_data_remove_outliers import remove_outliers
import field_mappings
from datetime import datetime, time, timedelta


def add_gps_data_with_timestamps(data, summary, custom_date):
    # GPS 데이터와 시간 인덱스를 가져옵니다.
    gps_data_list = eval(data[field_mappings.SENSOR_GPS_INDEX])

    # 이상치 제거
    gps_data_list = remove_outliers(gps_data_list)

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

