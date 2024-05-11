from collections import defaultdict
from datetime import datetime, time, timedelta
import field_mappings
import numpy as np
import math
#센서 데이터 리스트를 사용자 ID별로 분류합니다.
def classify_data_by_id(sensor_data_list):
    data_by_id = defaultdict(list)
    for data in sensor_data_list:
        data_by_id[data[field_mappings.SENSOR_ID_INDEX]].append(data)
    return data_by_id

def remove_outliers(gps_data):
    i = 1  # 첫 번째와 마지막 데이터는 비교 대상이 없으므로 중간 데이터부터 시작
    threshold = 0.0005  # 초기 이상치 판단 기준
    last_removed_index = -1  # 마지막으로 제거된 이상치의 인덱스 초기화
    
    while i < len(gps_data) - 1:
        # 제거된 이상치를 고려하여 이전 위치 결정
        if last_removed_index !=  -1:
            prev = last_removed_index  # 이상치가 제거된 위치
        else:
            prev = gps_data[i - 1]
        
        curr = gps_data[i]
        next = gps_data[i + 1]
        
        # 전후 데이터의 평균 위치 계산
        avg_lat = (prev[0] + next[0]) / 2
        avg_lon = (prev[1] + next[1]) / 2
        
        # 현재 위치와 평균 위치 사이의 거리 계산
        distance = math.sqrt((curr[0] - avg_lat)**2 + (curr[1] - avg_lon)**2)
        
        # 거리가 현재 threshold 이상 차이 나면 이상치로 간주
        if distance > threshold:
            gps_data[i - 1][2] += curr[2]  # 이전 데이터에 이상치 duration 추가
            gps_data.pop(i)  # 이상치 삭제
            last_removed_index = curr  # 마지막으로 이상치가 제거된 위치 저장
            print("이상치 제거: 위치 = ({}, {}), 새 기준 = {}".format(curr[0], curr[1], threshold))
        else:
            last_removed_index = -1  # 이상치가 아니면 리셋
            threshold = 0.0005  # 이상치 아니면 기준 리셋
            i += 1

    return gps_data
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
    summary[custom_date][category]['call_frequency'] += data[field_mappings.SENSOR_PHONE_FREQUENCY_INDEX]
    summary[custom_date][category]['call_duration'] += data[field_mappings.SENSOR_PHONE_DURATION_INDEX]
    sleeptime_screen_duration(summary,custom_date,data,category)
   
    if sum(illuminance_array) > 0:
        summary[custom_date][category]['illuminance_sum'] += avg_illuminance


def sleeptime_screen_duration(summary,custom_date,data,category):
    if category == 'sunset':
        if (data[field_mappings.SENSOR_HOUR_INDEX] in (22,23,0,1,2)):
            summary[custom_date]['sunset']['sleeptime_screen_duration'] += data[field_mappings.SENSOR_SCREEN_DURATION_INDEX]
            summary[custom_date]['sunset']['sleeptime_screen_duration_count'] += 1