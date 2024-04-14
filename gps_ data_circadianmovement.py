import numpy as np
import json
from astropy.timeseries import LombScargle
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime, timedelta

def load_gps_data_from_json(file_path):
    """
    JSON 파일에서 GPS 데이터를 로드합니다.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return np.array(data)  # 데이터를 numpy 배열로 변환

def preprocess_data(data):
    """
    GPS 데이터 전처리: 위도, 경도, 지속 시간, 시간을 분리하고, 시간을 타임스탬프로 변환합니다.
    """
    latitudes = []
    longitudes = []
    times = []
    durations = []  # 지속 시간을 저장할 리스트

    for entry in data:
        try:
            latitude, longitude, duration, time_str = entry  # 네 개의 요소를 각각 언패킹
            # 시간 문자열을 datetime 객체로 변환
            dt = datetime.fromisoformat(time_str)
            timestamp = (dt - datetime(1970, 1, 1)).total_seconds()
            latitudes.append(float(latitude))
            longitudes.append(float(longitude))
            durations.append(float(duration))  # 지속 시간 추가
            times.append(timestamp)
        except Exception as e:
            print(f"Skipping invalid entry: {entry}, Error: {e}")

    if not times:
        print("No valid time data available.")
        return None, None, None, None

    latitudes = np.array(latitudes)
    longitudes = np.array(longitudes)
    durations = np.array(durations)
    times = np.array(times)

    # 데이터 정렬
    sorted_indices = np.argsort(times)
    return latitudes[sorted_indices], longitudes[sorted_indices], durations[sorted_indices], times[sorted_indices]

def calculate_lomb_scargle(times, values):
    try:
        ls = LombScargle(times, values)
        frequency, power = ls.autopower()
        return frequency, power
    except Exception as e:
        print("Error in Lomb-Scargle calculation:", e)
        print("Times:", times)
        print("Values:", values)
        raise

def analyze_periodicity(data_day1, data_day2):
    latitudes1, longitudes1, durations1, times1 = preprocess_data(data_day1)
    latitudes2, longitudes2, durations2, times2 = preprocess_data(data_day2)

    if times1 is None or times2 is None:
        print("Invalid or insufficient data for analysis.")
        return None

    try:
        frequency1, power1 = calculate_lomb_scargle(times1, latitudes1)
        frequency2, power2 = calculate_lomb_scargle(times2, latitudes2)

        if not frequency1.size or not frequency2.size:
            print("No valid frequency data available for comparison.")
            return None

        common_frequencies = np.intersect1d(frequency1, frequency2)
        if common_frequencies.size == 0:
            print("No common frequencies found.")
            return None

        power1_common = np.array([power1[np.where(frequency1 == f)[0][0]] for f in common_frequencies])
        power2_common = np.array([power2[np.where(frequency2 == f)[0][0]] for f in common_frequencies])

        # 코사인 유사도 계산 전에 입력 배열의 비어 있는지 확인
        if power1_common.size == 0 or power2_common.size == 0:
            print("One of the power arrays is empty, cannot compute similarity.")
            return None

        similarity = cosine_similarity(power1_common.reshape(1, -1), power2_common.reshape(1, -1))[0][0]
        return similarity
    except Exception as e:
        print(f"Error during Lomb-Scargle analysis: {e}")
        return None


today = datetime.now().date()
yesterday = today - timedelta(days=1)

# 파일 경로 생성
file_path_day1 = f'./gps_data/2024-04-12/dongwook@naver.com.json'
file_path_day2 = f'./gps_data/2024-04-12/dongwook@naver.com.json'

data_day1 = load_gps_data_from_json(file_path_day1)
data_day2 = load_gps_data_from_json(file_path_day2)

similarity = analyze_periodicity(data_day1, data_day2)
print(f"Similarity between Day 1 and Day 2: {similarity}")

