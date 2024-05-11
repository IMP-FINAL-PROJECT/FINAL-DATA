import json
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from astropy.timeseries import LombScargle
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def plot_latitude_over_time(data, title):
    plt.figure(figsize=(12, 6))
    plt.plot(data['timestamp'], data['latitude'], marker='o', linestyle='-')
    plt.xlabel('Timestamp')
    plt.ylabel('Latitude')
    plt.title(title)
    plt.xticks(rotation=45)  # 타임스탬프 레이블을 회전하여 더 보기 쉽게 만듦
    plt.tight_layout()  # 레이아웃 조정
    plt.grid(True)  # 그리드 추가
    plt.show()

def plot_frequency_power(frequency1, power1, frequency2, power2, label1='Day 1', label2='Day 2'):
    plt.figure(figsize=(12, 6))
    plt.plot(frequency1, power1, label=label1)
    plt.plot(frequency2, power2, label=label2)
    plt.xlabel('Frequency')
    plt.ylabel('Power')
    plt.title('Comparison of Lomb-Scargle Power Spectra')
    plt.legend()
    plt.grid(True)
    plt.show()

def create_regular_intervals(data, interval_seconds=10):
    result_df = pd.DataFrame(columns=['latitude', 'longitude', 'timestamp'])
    
    for i in range(len(data)):
        start_lat, start_lon, start_duration, start_time = data[i]
        start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S.%f" if '.' in start_time else "%Y-%m-%dT%H:%M:%S")
        duration_seconds = start_duration / 1000
        end_time = start_time + timedelta(seconds=duration_seconds)
        
        while start_time <= end_time:
            result_df = result_df.append({'latitude': start_lat, 'longitude': start_lon, 'timestamp': start_time}, ignore_index=True)
            start_time += timedelta(seconds=interval_seconds)

    result_df.set_index('timestamp', inplace=True)
    result_df = result_df.resample(f'{interval_seconds}S').first()
    result_df.interpolate(method='time', inplace=True)

    return result_df.reset_index()

def load_and_process_gps_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    processed_data = create_regular_intervals(data)
    return processed_data

def perform_multidimensional_lomb_scargle(times, latitudes, longitudes):
    frequency_lat, power_lat = LombScargle(times, latitudes).autopower()
    frequency_lon, power_lon = LombScargle(times, longitudes).autopower()
    return (frequency_lat, power_lat), (frequency_lon, power_lon)

def calculate_similarity(frequency1, power1, frequency2, power2):
    common_frequency = np.linspace(min(frequency1.min(), frequency2.min()), max(frequency1.max(), frequency2.max()), num=max(len(frequency1), len(frequency2)))
    interp_power1 = np.interp(common_frequency, frequency1, power1)
    interp_power2 = np.interp(common_frequency, frequency2, power2)
    interp_power1 = interp_power1.reshape(1, -1)
    interp_power2 = interp_power2.reshape(1, -1)
    similarity = cosine_similarity(interp_power1, interp_power2)[0][0]
    return similarity

# 파일 경로
file_path_day1 = './gps_data/2024-04-08/dongwook@naver.com.json'
file_path_day2 = './gps_data/2024-04-09/dongwook@naver.com.json'

# 데이터 로드
processed_data1 = load_and_process_gps_data(file_path_day1)
processed_data2 = load_and_process_gps_data(file_path_day2)

# 다차원 Lomb-Scargle 분석 수행
(lat_frequency1, lat_power1), (lon_frequency1, lon_power1) = perform_multidimensional_lomb_scargle(
    processed_data1['timestamp'].astype(int), processed_data1['latitude'], processed_data1['longitude']
)
(lat_frequency2, lat_power2), (lon_frequency2, lon_power2) = perform_multidimensional_lomb_scargle(
    processed_data2['timestamp'].astype(int), processed_data2['latitude'], processed_data2['longitude']
)

# 유사도 계산
similarity_lat = calculate_similarity(lat_frequency1, lat_power1, lat_frequency2, lat_power2)
similarity_lon = calculate_similarity(lon_frequency1, lon_power1, lon_frequency2, lon_power2)

# 결과 출력
print(f"The similarity between the two days based on latitude data is: {similarity_lat:.2f}")
print(f"The similarity between the two days based on longitude data is: {similarity_lon:.2f}")

# 시각화
plot_latitude_over_time(processed_data1, 'Latitude Over Time for Day 1')
plot_latitude_over_time(processed_data2, 'Latitude Over Time for Day 2')
plot_frequency_power(lat_frequency1, lat_power1, lat_frequency2, lat_power2, label1='Day 1 Latitude', label2='Day 2 Latitude')
plot_frequency_power(lon_frequency1, lon_power1, lon_frequency2, lon_power2, label1='Day 1 Longitude', label2='Day 2 Longitude')
# 두 유사도 값을 하나로 결합하여 평균 유사도 계산
def combine_similarities(similarity1, similarity2):
    return (similarity1 + similarity2) / 2

# 유사도 계산
combined_similarity = combine_similarities(similarity_lat, similarity_lon)

# 결합된 유사도 결과 출력
print(f"The combined similarity between the two days is: {combined_similarity:.2f}")
