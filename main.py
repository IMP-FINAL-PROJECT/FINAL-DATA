from collections import defaultdict
from datetime import datetime,time,timedelta
from excel_data_loader import get_sunrise_sunset, round_up_time

def aggregate_sensor_data(sensor_data_list):
    # 초기 데이터 구조 설정
    user_aggregate_data = defaultdict(lambda: {'pedometer': 0, 'screen_frequency': 0, 'screen_duration': 0, 'count': 0})
    
    # 각 데이터 항목을 순회하며 해당 값을 합산
    for data in sensor_data_list:
        id = data[1]  # 사용자 ID
        pedometer = data[3]  # pedometer 값
        screen_frequency = data[4]  # screen_frequency 값
        screen_duration = data[5]  # screen_duration 값

        # 사용자별 데이터 집계
        user_aggregate_data[id]['pedometer'] += pedometer
        user_aggregate_data[id]['screen_frequency'] += screen_frequency
        user_aggregate_data[id]['screen_duration'] += screen_duration
        user_aggregate_data[id]['count'] += 1
    
    return user_aggregate_data

def classify_and_summarize_data(sensor_data_list):
    # 아이디별로 데이터 분류
    data_by_id = defaultdict(list)
    for data in sensor_data_list:
        id = data[1]
        data_by_id[id].append(data)
    
    summary = defaultdict(lambda: defaultdict(lambda: {'daytime': 0, 'sunset': 0}))

    for id, data_list in data_by_id.items():
        # 날짜별로 데이터 분류
        data_by_date = defaultdict(list)
        for data in data_list:
            timestamp = data[7]
            date_str = timestamp.strftime('%Y-%m-%d')
            data_by_date[date_str].append(data)
        
        for date_str, daily_data_list in data_by_date.items():
            current_date = datetime.strptime(date_str, '%Y-%m-%d')
            next_date = current_date + timedelta(days=1)
            MMDD_today = current_date.strftime('%m%d')
            MMDD_next = next_date.strftime('%m%d')

            sunrise_today, _ = get_sunrise_sunset(MMDD_today)
            sunrise_next, _ = get_sunrise_sunset(MMDD_next)
          
            # 다음 날의 일출 시간을 구하기 위해 일출 시간을 '시'로만 올림 처리
            if sunrise_next != "No data available for the given date.":
                rounded_sunrise_next = round_up_time(sunrise_next)
                rounded_sunrise_today = round_up_time(sunrise_today)
                # 다음 날 일출 시간을 현재 날짜와 합쳐 완전한 datetime 객체 생성
                sunrise_next_time = datetime.combine(next_date, datetime.min.time()) + timedelta(hours=rounded_sunrise_next)


                sunrise_today_time = datetime.combine(current_date, datetime.min.time()) + timedelta(hours=rounded_sunrise_today)
            for data in daily_data_list:
                date_part = data[7]
                hour_part = data[8]
                timestamp = datetime.combine(date_part, time(hour_part))
                if sunrise_today != "No data available for the given date." and sunrise_today_time<timestamp < sunrise_next_time:
                    # 현재 날짜의 일출 시간 이후, 다음 날의 일출 시간 이전 데이터
                    summary[id][date_str]['daytime'] += 1
                else:
                    print("asdasdasd")
                    # 그 외 시간(주로 다음 날 일출 전의 밤 시간)
                    summary[id][date_str]['sunset'] += 1
    
    return summary

# 센서 데이터 리스트 예시
# sensor_data_list = [...]
import datacall
batch_sensor_data_start_num = datacall.get_latest_start_num()
sensor_data_list = datacall.get_sensor_data(batch_sensor_data_start_num)
# classify_and_summarize_data 함수 사용
summary_data = classify_and_summarize_data(sensor_data_list)

# 요약 데이터 출력
for id, dates in summary_data.items():
    for date, periods in dates.items():
        print(f"ID: {id}, Date: {date}, Daytime Count: {periods['daytime']}, Sunset Count: {periods['sunset']}")