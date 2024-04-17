import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from scipy.signal import lombscargle

def create_regular_intervals(data, interval_seconds=3600):
    timestamps = []
    latitudes = []
    longitudes = []

    for entry in data:
        latitude = entry[0]
        longitude = entry[1]
        duration_ms = entry[2]
        start_time_str = entry[3]
        start_time = datetime.fromisoformat(start_time_str)

        duration_seconds = duration_ms / 1000
        num_intervals = int(np.ceil(duration_seconds / interval_seconds))

        for i in range(num_intervals):
            time = start_time + timedelta(seconds=i * interval_seconds)
            timestamps.append(time)
            latitudes.append(latitude)
            longitudes.append(longitude)

    df = pd.DataFrame({
        'timestamp': timestamps,
        'latitude': latitudes,
        'longitude': longitudes
    })
    
    df.set_index('timestamp', inplace=True)
    df.sort_index(inplace=True)
    df = df.resample(f'{interval_seconds}s').mean().interpolate()
    return df

def load_and_process_gps_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return create_regular_intervals(data)

def save_to_excel(df, output_path):
    df.to_excel(output_path)

# 파일 경로 설정
file_paths = [
    './gps_data/2024-04-06/dongwook@naver.com.json',
    './gps_data/2024-04-07/dongwook@naver.com.json',
    './gps_data/2024-04-08/dongwook@naver.com.json',
]

# 각 파일에서 데이터를 처리하고 모든 데이터프레임을 하나의 리스트에 저장
dataframes = [load_and_process_gps_data(file_path) for file_path in file_paths]

# 모든 데이터프레임을 하나로 결합
combined_data = pd.concat(dataframes)
combined_data.reset_index(inplace=True)  # 인덱스 리셋
combined_data['number'] = np.arange(1, len(combined_data) + 1)  # 순차적인 번호 추가
'''
combined_data.to_csv('output.csv', index=False)
raise
'''
# Assume 'number' and 'latitude' are columns from your 'combined_data' DataFrame
number = combined_data['number'].values  # This should be the 'number' column
latitude = combined_data['latitude'].values  # This should be the 'latitude' column
# 'latitude' 열의 데이터를 numpy 배열로 가져옵니다.
latitude = combined_data['latitude'].values
'''
# Min-Max 정규화를 사용하여 위도 데이터를 0과 1 사이의 값으로 스케일링합니다.
latitude_min = latitude.min()
latitude_max = latitude.max()
latitude = (latitude - latitude_min) / (latitude_max - latitude_min)
'''
# Frequency range for the Lomb-Scargle periodogram
#freq = np.linspace(1, int(len(combined_data)), int(len(combined_data)))
freq = np.linspace(0.1, 24, 24)

# Calculate Lomb-Scargle periodogram
pgram = lombscargle(number, latitude, freq, normalize=True)

# Plotting
fig, (ax_t, ax_w) = plt.subplots(2, 1, constrained_layout=True)

# Time-domain plot
ax_t.plot(number, latitude, 'bo')
ax_t.set_title('The Lomb-Scargle periodogram')
ax_t.set_xlabel('Time')
ax_t.set_ylabel('Latitude')

# Frequency-domain plot (Lomb-Scargle periodogram)
ax_w.plot(freq, pgram)
ax_w.set_xlabel('Frequency')
ax_w.set_ylabel('Normalized Amplitude')

# Display the plot
plt.show()
