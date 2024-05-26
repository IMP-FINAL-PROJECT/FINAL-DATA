from .config import SENSOR_ID_INDEX, SENSOR_ILLUMINANCE_INDEX, SENSOR_PEDOMETER_INDEX, SENSOR_SCREEN_FREQUENCY_INDEX, SENSOR_SCREEN_DURATION_INDEX, SENSOR_PHONE_FREQUENCY_INDEX, SENSOR_PHONE_DURATION_INDEX, SENSOR_GPS_INDEX, SENSOR_TIMESTAMP_INDEX, SENSOR_HOUR_INDEX
from GPS_Data_Processing.gps_data_add_timestamp import add_gps_data_with_timestamps


#개별 데이터 합산 및 처리 함수 
def process_data_point(data, summary, custom_date, category):
    illuminance_array = eval(data[SENSOR_ILLUMINANCE_INDEX])
    avg_illuminance = sum(illuminance_array) / len(illuminance_array) if illuminance_array else 0

    summary[custom_date][category]['count'] += 1
    #summary[custom_date]['gps']['gps'].extend(gps_data_list)
    add_gps_data_with_timestamps(data, summary, custom_date)
    summary[custom_date]['gps']['confirm'].append(data[SENSOR_HOUR_INDEX])
    summary[custom_date][category]['pedometer'] += data[SENSOR_PEDOMETER_INDEX]
    summary[custom_date][category]['screen_frequency'] += data[SENSOR_SCREEN_FREQUENCY_INDEX]
    summary[custom_date][category]['screen_duration'] += data[SENSOR_SCREEN_DURATION_INDEX]
    summary[custom_date][category]['call_frequency'] += data[SENSOR_PHONE_FREQUENCY_INDEX]
    summary[custom_date][category]['call_duration'] += data[SENSOR_PHONE_DURATION_INDEX]
    sleeptime_screen_duration(summary,custom_date,data,category)
   
    if sum(illuminance_array) > 0:
        summary[custom_date][category]['illuminance_sum'] += avg_illuminance


def sleeptime_screen_duration(summary,custom_date,data,category):
    if category == 'sunset':
        if (data[SENSOR_HOUR_INDEX] in (22,23,0,1,2)):
            summary[custom_date]['sunset']['sleeptime_screen_duration'] += data[SENSOR_SCREEN_DURATION_INDEX]
            summary[custom_date]['sunset']['sleeptime_screen_duration_count'] += 1