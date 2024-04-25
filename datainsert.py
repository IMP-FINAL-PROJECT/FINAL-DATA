import mysqlconnect
from datetime import datetime

def insert_dailylifepattern_data(data):
    """
    주어진 start_num을 기준으로 sensor 테이블에서 모든 레코드를 가져오는 함수
    """
    values_to_insert = []
    for id, dates in data.items():
        for date, periods in dates.items():

        # ID와 날짜는 직접 사용
        # Daytime Count, Sunset Count, Cluster 등은 periods 딕셔너리에서 추출
            daytime_count = periods['daytime']['count']
            daytime_illuminance_avg = periods['daytime']['illuminance_avg']  # 예시 데이터에는 0으로 되어 있지만, 필요에 따라 계산할 수 있음
            daytime_pedometer = periods['daytime']['pedometer']
            daytime_screen_frequency = periods['daytime']['screen_frequency']
            daytime_screen_duration = periods['daytime']['screen_duration']
            daytime_call_frequency = periods['daytime']['call_frequency']
            daytime_call_duration = periods['daytime']['call_duration']
        
        # sunset 및 gps 관련 데이터 추출 (실제 데이터 구조에 맞게 조정 필요)
            sunset_count = periods['sunset']['count']
            sunset_illuminance_avg = periods['sunset']['illuminance_avg']  # 필요에 따라 계산
            sunset_pedometer = periods['sunset']['pedometer']
            sunset_screen_frequency = periods['sunset']['screen_frequency']
            sunset_screen_duration = periods['sunset']['screen_duration']
            sunset_call_frequency = periods['sunset']['call_frequency']
            sunset_call_duration = periods['sunset']['call_duration']
        
            gps_cluster = str(periods['gps']['cluster'])  # 실제 데이터 구조에 맞게 조정
            home_stay_percentage = periods['gps']['homestay']  # 실제 데이터 구조에 맞게 조정
            hour_index = str(periods['gps']['confirm'])  # 실제 데이터 구조에 맞게 조정
        
        # 튜플 형태로 values_to_insert 리스트에 추가
        # 아래 예시는 각 컬럼에 대응하는 값의 순서와 갯수가 맞지 않을 수 있으므로, 실제 데이터베이스 구조에 맞게 조정 필요
            values_to_insert.append((
                id,
                gps_cluster,
                home_stay_percentage,
                "test",
                daytime_screen_frequency, 
                sunset_screen_frequency,
                daytime_screen_duration, 
                sunset_screen_duration, 
                daytime_call_frequency,
                sunset_call_frequency,
                daytime_call_duration,
                sunset_call_duration,
                daytime_illuminance_avg,
                sunset_illuminance_avg,          
                daytime_pedometer, 
                sunset_pedometer, 
                daytime_count, 
                sunset_count, 
                hour_index,
                date        
            ))
    insert_query = """
    INSERT INTO daily_life_pattern (id, place_diversity, home_stay_percentage, life_routine_consistency, day_phone_use_frequency, night_phone_use_frequency, day_phone_use_duration, night_phone_use_duration,day_call_use_frequency, night_call_use_frequency,  day_call_use_duration, night_call_use_duration, day_light_exposure, night_light_exposure, day_step_count, night_step_count, day_time_count, night_time_count, hour_index, date)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    mysqlconnect.executemany_query(insert_query,values_to_insert)





def insert_lastnum(lastnum):
    # 현재 날짜와 시간을 가져옴
    now = datetime.now()

    # 타임스탬프를 'YYYY-MM-DD HH:MM:SS' 형식의 문자열로 변환
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    # INSERT 쿼리에 lastnum과 현재 타임스탬프 포함
    insert_query = f"""
    INSERT INTO batch (start_num, timestamp) VALUES ({lastnum+1}, '{timestamp}');
    """
    mysqlconnect.execute_insert_query(insert_query)
    print("Inserted with timestamp")
