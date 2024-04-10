from summary_main import classify_and_summarize_data
from excel_data_loader import get_sunrise_sunset, round_up_time
from datadelete import delete_existing_entries
from mysqlconnect import execute_val_query
from summary_main import  classify_and_summarize_data
from datainsert import insert_dailylifepattern_data, insert_lastnum
from dataselect import query_existing_id_date_combinations
from data_filter import filter_existing_entries
from data_fetch import fetch_data_for_sunrise_intervals




import datacall
batch_sensor_data_start_num = datacall.get_latest_start_num()
sensor_data_list = datacall.get_sensor_data(batch_sensor_data_start_num)
existing_combinations = query_existing_id_date_combinations()
# summary_data에서 이미 존재하는 항목 필터링
existing_entries = filter_existing_entries(sensor_data_list, existing_combinations)
delete_existing_entries(existing_entries)
fetched_data =fetch_data_for_sunrise_intervals(existing_entries, batch_sensor_data_start_num)
# 결과 출력
sensor_data_list+=tuple(fetched_data)
summary_data = classify_and_summarize_data(sensor_data_list)
insert_dailylifepattern_data(summary_data)
insert_lastnum(sensor_data_list[-1][0])