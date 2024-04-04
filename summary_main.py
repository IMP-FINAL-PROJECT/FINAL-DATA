from datetime import datetime, time
from data_classification import classify_data_by_id, get_custom_date_and_category, process_data_point
from summary_calculation import calculate_averages
from excel_data_loader import get_sunrise_sunset, round_up_time
from gps_data_map import create_and_save_map
from collections import defaultdict
from gps_data_clustering import perform_dbscan_clustering


def classify_and_summarize_data(sensor_data_list):
    data_by_id = classify_data_by_id(sensor_data_list)
    summary = defaultdict(lambda: defaultdict(lambda: {
        'gps': {'count': 0, 'gps': [],'map': '', 'confirm':[], 'cluster':[]},
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
                
        create_and_save_map(summary[id][custom_date]['gps']['gps'], id, custom_date)
        for date, categories in summary[id].items():
            gps_data = categories['gps']['gps']
            if gps_data:
                cluster_ratios = perform_dbscan_clustering(gps_data)
                if cluster_ratios:
                    summary[id][date]['gps']['cluster'] = cluster_ratios
                map_file_path = create_and_save_map(gps_data, id, date)
                if map_file_path:
                    summary[id][date]['gps']['map'] = map_file_path



    return summary



import datacall
batch_sensor_data_start_num = datacall.get_latest_start_num()
sensor_data_list = datacall.get_sensor_data(batch_sensor_data_start_num)
# classify_and_summarize_data 함수 사용
summary_data = classify_and_summarize_data(sensor_data_list)

# 요약 데이터 출력
for id, dates in summary_data.items():
    for date, periods in dates.items():
        print(f"ID: {id}, Date: {date}, Daytime Count: {periods['daytime']}, Sunset Count: {periods['sunset']}, Cluster: {periods['gps']['cluster']}")