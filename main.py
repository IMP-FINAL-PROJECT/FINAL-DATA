from collections import defaultdict

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

# 가정한 데이터 입력 예시
import datacall
batch_sensor_data_start_num = datacall.get_latest_start_num()
sensor_data_list = datacall.get_sensor_data(batch_sensor_data_start_num)

# 데이터 합산 함수 사용
user_aggregate_data = aggregate_sensor_data(sensor_data_list)

# 결과 출력
for id, aggregate in user_aggregate_data.items():
    print(f"ID: {id}, Pedometer Sum: {aggregate['pedometer']}, Screen Frequency Sum: {aggregate['screen_frequency']}, Screen Duration Sum: {aggregate['screen_duration']}, Count: {aggregate['count']}")
