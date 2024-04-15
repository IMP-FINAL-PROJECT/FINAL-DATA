import json
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
from astropy.timeseries import LombScargle
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd



def load_and_process_gps_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    # 10초 간격으로 데이터 재생성
    processed_data = create_regular_intervals(data)
    return processed_data


def create_regular_intervals(data, interval_seconds=10):
    # 결과를 저장할 데이터프레임 초기화
    result_df = pd.DataFrame(columns=['latitude', 'longitude', 'timestamp'])
    
    # 데이터를 반복하며 각 구간에 대해 데이터 포인트 생성
    for i in range(len(data)):
        start_lat, start_lon, start_duration, start_time = data[i]
        start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S.%f" if '.' in start_time else "%Y-%m-%dT%H:%M:%S")
        duration_seconds = start_duration / 1000
        end_time = start_time + timedelta(seconds=duration_seconds)
        
        # 각 인터벌에 대한 타임스탬프 생성
        while start_time <= end_time:
            result_df = result_df.append({'latitude': start_lat, 'longitude': start_lon, 'timestamp': start_time}, ignore_index=True)
            start_time += timedelta(seconds=interval_seconds)

    # 데이터프레임의 타임스탬프를 인덱스로 설정
    result_df.set_index('timestamp', inplace=True)
    
    # 필요에 따라 resample 후 보간
    result_df = result_df.resample(f'{interval_seconds}S').first()  # 10초 간격으로 리샘플
    result_df.interpolate(method='time', inplace=True)  # 시간 기반 보간 사용

    return result_df.reset_index()



# 파일 경로
file_path_day1 = './gps_data/2024-04-13/joowon@naver.com.json'
file_path_day2 = './gps_data/2024-04-14/joowon@naver.com.json'


# 데이터 로드
processed_data1 = load_and_process_gps_data(file_path_day1)
processed_data2 = load_and_process_gps_data(file_path_day2)
