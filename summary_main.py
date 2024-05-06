from datetime import datetime, time
from data_classification import classify_data_by_id, get_custom_date_and_category, process_data_point
from summary_calculation import calculate_averages
from excel_data_loader import get_sunrise_sunset, round_up_time
from gps_data_map import create_and_save_map
from collections import defaultdict
from gps_data_clustering import perform_dbscan_clustering
from datainsert import insert_dailylifepattern_data, insert_lastnum
from gps_data_homestay import homestay_percentage
from gps_data_save import save_gps_data
from sample import circadianmovement_main
import field_mappings


def classify_and_summarize_data(sensor_data_list):
    data_by_id = classify_data_by_id(sensor_data_list)
    summary = defaultdict(lambda: defaultdict(lambda: {
        'gps': {'count': 0, 'gps': [],'map': '', 'confirm':[], 'cluster':[], 'homestay':0, 'life_routine_consistency':0},
        'daytime': {'count': 0, 'illuminance_sum': 0, 'illuminance_avg': 0, 'pedometer': 0, 'screen_frequency': 0, 'screen_duration': 0, 'call_frequency': 0, 'call_duration': 0},
        'sunset': {'count': 0, 'illuminance_sum': 0, 'illuminance_avg': 0, 'pedometer': 0, 'screen_frequency': 0, 'screen_duration': 0, 'call_frequency': 0, 'call_duration': 0,'sleeptime_screen_duration':0,'sleeptime_screen_duration_count':0},
        'score': {'activity_score': 0, 'phone_usage_frequency_score': 0, 'phone_usage_duration_score': 0, 'call_duration_score': 0, 'illumination_exposure_score': 0, 'location_diversity_score': 0, 'homestay_score': 0}
    }))

    for id, data_list in data_by_id.items():
        for data in data_list:
            current_date = data[field_mappings.SENSOR_TIMESTAMP_INDEX]
            sunrise_today, sunset_today = get_sunrise_sunset(current_date.strftime('%m%d'))
            if sunrise_today != "No data available for the given date." and sunset_today != "No data available for the given date.":
                rounded_sunrise_today = round_up_time(sunrise_today)
                rounded_sunset_today = round_up_time(sunset_today)
                sunrise_today_time = datetime.combine(current_date, time(rounded_sunrise_today, 0))
                sunset_today_time = datetime.combine(current_date, time(rounded_sunset_today, 0))
                
                timestamp = datetime.combine(data[field_mappings.SENSOR_TIMESTAMP_INDEX], time(data[field_mappings.SENSOR_HOUR_INDEX]))
                custom_date, category = get_custom_date_and_category(timestamp, sunrise_today_time, sunset_today_time, current_date)
                process_data_point(data, summary[id], custom_date, category)
        create_and_save_map(summary[id][custom_date]['gps']['gps'], id, custom_date)
        for date, categories in summary[id].items():
            gps_data = categories['gps']['gps']
            if gps_data:
                file_path = save_gps_data(gps_data, id, date)
                summary[id][date]['gps']['data_file'] = file_path
                cluster_ratios = perform_dbscan_clustering(gps_data)
                if cluster_ratios:
                    summary[id][date]['gps']['cluster'] = cluster_ratios
                    home_stay_ratio = homestay_percentage(id,cluster_ratios)
                    if home_stay_ratio:
                        summary[id][date]['gps']['homestay'] = home_stay_ratio
                map_file_path = create_and_save_map(gps_data, id, date)
                if map_file_path:
                    summary[id][date]['gps']['map'] = map_file_path

            if len(categories['gps']['confirm']) > 22:
                summary[id][date]['gps']['life_routine_consistency'] = circadianmovement_main(date,id)


        calculate_averages(summary[id])
        calculate_scores(summary[id])
    return summary

def calculate_scores(summary):
    for user, data in summary.items():
        data['score']['activity_score'] = data['daytime']['pedometer'] + data['sunset']['pedometer']
        data['score']['phone_usage_frequency_score'] = calculate_phone_usage_frequency_score((data['daytime']['screen_frequency'] + (data['sunset']['screen_frequency'] * 2))/3)
        data['score']['phone_usage_duration_score'] = calculate_phone_usage_duration_score((data['daytime']['screen_duration'] + (data['sunset']['screen_duration'] * 2))/3)
        data['score']['call_duration_score'] = data['daytime']['call_duration'] - data['sunset']['call_duration']
        data['score']['illumination_exposure_score'] = data['daytime']['illuminance_avg'] + data['sunset']['illuminance_avg']
        data['score']['location_diversity_score'] = calculate_location_diversity(data['gps']['cluster'])  # 가정된 함수
        data['score']['homestay_score'] = calculate_homestay_score(data['gps']['homestay'])  # 가정된 함수

# 장소 다양성 점수 계산 함수
def calculate_location_diversity(clusters):
    # 장소 다양성을 계산하는 로직을 구현 (예: 클러스터의 개수나 다양성 지수)
    return 10  # 예시로 클러스터의 유니크한 개수를 점수로 사용

# 집에 머무는 시간 점수 계산 함수
def calculate_homestay_score(homestay_hours):
    # 집에 머무는 시간에 대한 점수 계산 (예: 머문 시간이 길면 낮은 점수)
    max_hours = 24  # 하루 최대 시간
    return 10  # 예시로 최대 시간에서 머문 시간을 빼서 점수 계산

def calculate_phone_usage_frequency_score(frequency):
    # 최소 점수는 0, 최대 점수는 100
    max_score = 100
    max_frequency = 10  # 최대 기준치

    if frequency >= max_frequency:
        return max_score
    else:
        # 선형 스케일로 점수 계산 (frequency / max_frequency) * max_score
        return (frequency / max_frequency) * max_score
    
def calculate_phone_usage_duration_score(duration):
    # 15분을 ms로 변환 
    max_duration = 15 * 60 * 1000  
    max_score = 100  # 최대 점수

    if duration >= max_duration:
        return max_score
    else:
        # 선형 스케일로 점수 계산 (duration / max_duration) * max_score
        return (duration / max_duration) * max_score


import datacall
batch_sensor_data_start_num = datacall.get_latest_start_num()
batch_sensor_data_start_num=0
sensor_data_list = datacall.get_sensor_data(batch_sensor_data_start_num)
summary_data = classify_and_summarize_data(sensor_data_list)
#insert_dailylifepattern_data(summary_data)
#insert_lastnum(sensor_data_list[-1][0])

for id, dates in summary_data.items():
    for date, periods in dates.items():
        print(f"ID: {id}, Date: {date}, Daytime Count: {periods['score']}")
