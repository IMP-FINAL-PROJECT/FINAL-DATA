from datetime import datetime, time
from Data_Manage.data_classification import classify_data_by_id, get_custom_date_and_category, process_data_point
from .summary_calculation import calculate_averages
from Utile.excel_data_loader import get_sunrise_sunset, round_up_time
from GPS_Data_Processing.gps_data_map import create_and_save_map
from collections import defaultdict
from GPS_Data_Processing.gps_data_clustering import perform_dbscan_clustering
from Data_Manage.data_insert import insert_dailylifepattern_data, insert_lastnum
from GPS_Data_Processing.gps_data_homestay import homestay_percentage
from GPS_Data_Processing.gps_data_save import save_gps_data
from GPS_Data_Processing.gps_data_circadianmovement import circadianmovement_main
from Scoring.calculate_scores import calculate_scores
import field_mappings


def classify_and_summarize_data(sensor_data_list):
    data_by_id = classify_data_by_id(sensor_data_list)
    summary = defaultdict(lambda: defaultdict(lambda: {
        'gps': {'count': 0, 'gps': [],'map': '', 'confirm':[], 'cluster':[], 'homestay':0, 'life_routine_consistency':0},
        'daytime': {'count': 0, 'illuminance_sum': 0, 'illuminance_avg': 0, 'pedometer': 0, 'screen_frequency': 0, 'screen_duration': 0, 'call_frequency': 0, 'call_duration': 0},
        'sunset': {'count': 0, 'illuminance_sum': 0, 'illuminance_avg': 0, 'pedometer': 0, 'screen_frequency': 0, 'screen_duration': 0, 'call_frequency': 0, 'call_duration': 0,'sleeptime_screen_duration':0,'sleeptime_screen_duration_count':0},
        'score': {'activity_score': 0, 'phone_usage_score': 0, 'illumination_exposure_score': 0, 'location_diversity_score': 0, 'circadian_rhythm_score': 0}
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

# import datacall
# batch_sensor_data_start_num = datacall.get_latest_start_num()
# batch_sensor_data_start_num=0
# sensor_data_list = datacall.get_sensor_data(batch_sensor_data_start_num)
# summary_data = classify_and_summarize_data(sensor_data_list)
# #insert_dailylifepattern_data(summary_data)
# #insert_lastnum(sensor_data_list[-1][0])

# for id, dates in summary_data.items():
#     for date, periods in dates.items():
#         print(f"ID: {id}, Date: {date}, Daytime Count: {periods['score']}")
