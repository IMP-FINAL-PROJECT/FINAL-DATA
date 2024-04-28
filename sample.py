import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from scipy.signal import lombscargle

# Global parameters
no_of_past_days = 5
hours_a_day =144
select_circadianmovement = [100,200,300,400,600,800,1200,2400]
weight_circadianmovement = [8,7,6,5,4,3,2,1]
margin_window=30
def compute_ECM(data, margin_window_begin=70, margin_window_end=130):
    result = sum(data[margin_window_begin:margin_window_end]) 
    return result

def weight_compute_ECM(data):
    result=0
    for i in select_circadianmovement:
        result+=sum(data[i-margin_window:i+margin_window])*weight_circadianmovement[select_circadianmovement.index(i)]
    return result/sum(weight_circadianmovement)

def create_regular_intervals(data, interval_seconds=int(86400/hours_a_day)):
    timestamps, latitudes, longitudes = [], [], []
    for entry in data:
        latitude, longitude, duration_ms, start_time_str = entry
        start_time = datetime.fromisoformat(start_time_str)
        duration_seconds = duration_ms / 1000
        num_intervals = int(np.ceil(duration_seconds / interval_seconds))

        for i in range(num_intervals):
            time = start_time + timedelta(seconds=i * interval_seconds)
            timestamps.append(time)
            latitudes.append(latitude)
            longitudes.append(longitude)

    df = pd.DataFrame({'timestamp': timestamps, 'latitude': latitudes, 'longitude': longitudes})
    df.set_index('timestamp', inplace=True)
    df.sort_index(inplace=True)
    
    # Check if the number of records is less than 80% of hours_a_day
    if len(df) < hours_a_day * 0.7:
        return   # Return None if data is insufficient

    df = df.resample(f'{interval_seconds}s').mean().interpolate()
    return df


def generate_file_paths(base_date, days, id):
    if isinstance(base_date, str):
        base_date = datetime.fromisoformat(base_date)
    file_paths = []
    # 시작 날짜를 기준으로 과거에서 현재로 날짜를 생성합니다.
    for i in range(days):
        # 과거로 갈수록 더 큰 i를 빼주어 최근 날짜로 가까워지게 합니다.
        date = base_date - timedelta(days=days - 1 - i)
        file_path = f'./gps_data/{date.strftime("%Y-%m-%d")}/{id}.json'
        #file_path = f'./gps_data/2024-04-11/{id}.json'
        file_paths.insert(0, file_path)
    return file_paths


def load_and_process_gps_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return create_regular_intervals(data)
    except FileNotFoundError:
        return
    
def save_to_excel(df, output_path):
    df.to_excel(output_path)
    
def plot_circadian_movement(time, latitude, longitude, pgram_latitude, pgram_longitude):
    fig, axs = plt.subplots(4, 1, figsize=(10, 12), constrained_layout=True)

    # Time-domain plot for Latitude
    axs[0].plot(time, latitude, 'bo')
    axs[0].set_title('Time-Domain Plot (Latitude)')
    axs[0].set_xlabel('Time')
    axs[0].set_ylabel('Latitude')

    # Frequency-domain plot for Latitude
    axs[1].plot(pgram_latitude)
    axs[1].set_title('Lomb-Scargle Periodogram (Latitude)')
    axs[1].set_xlabel('Angular frequency')
    axs[1].set_ylabel('Normalized amplitude')

    # Time-domain plot for Longitude
    axs[2].plot(time, longitude, 'go')
    axs[2].set_title('Time-Domain Plot (Longitude)')
    axs[2].set_xlabel('Time')
    axs[2].set_ylabel('Longitude')

    # Frequency-domain plot for Longitude
    axs[3].plot(pgram_longitude)
    axs[3].set_title('Lomb-Scargle Periodogram (Longitude)')
    axs[3].set_xlabel('Angular frequency')
    axs[3].set_ylabel('Normalized amplitude')

    plt.show()

def circadianmovement_main(base_date, id):
    # Generate paths for up to twice the number of required days
    file_paths = generate_file_paths(base_date, no_of_past_days * 2, id)
    
    # Initialize list to keep track of the dates used in the analysis
    successful_dates = []
    
    # Attempt to load data
    dataframes = []
    for file_path in file_paths:
        df = load_and_process_gps_data(file_path)
        if df is not None:
            dataframes.append(df)
            # Extract and store the date from the file path if the data load was successful
            date_from_path = file_path.split('/')[-2]  # Assumes file path format "./gps_data/YYYY-MM-DD/id.json"
            successful_dates.append(date_from_path)
    
    # Check if we have at least the required number of samples
    if len(dataframes) < no_of_past_days:
        print("Insufficient data to perform analysis. Returning 0.")
        return 0

    # Limit the number of days to the first 5 valid dataframes
    dataframes = dataframes[:no_of_past_days]
    successful_dates = successful_dates[:no_of_past_days]  # Also limit the dates list to the used dataframes

    dataframes.reverse()  # Reverse the order of dataframes
    successful_dates.reverse()
    # Combine the available data
    combined_data = pd.concat(dataframes)
    combined_data.reset_index(inplace=True)

    required_samples = no_of_past_days * hours_a_day
    if len(combined_data) < required_samples:
        # If there are not enough records, try to interpolate
        if len(combined_data) > 0:
            extended_time = pd.date_range(start=combined_data['timestamp'].min(), periods=required_samples, freq=f'{int(3600*24/hours_a_day)}S')
            combined_data.set_index('timestamp', inplace=True)
            combined_data = combined_data.reindex(extended_time).interpolate().reset_index()
        else:
            print("Not enough data points even after extending the range. Returning 0.")
            return 0
    else:
        combined_data = combined_data.head(required_samples)

    combined_data['number'] = np.arange(1, len(combined_data) + 1)
    
    # Prepare data for Lomb-Scargle periodogram
    time = np.linspace(0, no_of_past_days * (2 * np.pi), required_samples)
    latitude = combined_data['latitude'].values
    longitude = combined_data['longitude'].values

    # Normalize the data
    latitude = (latitude - latitude.mean())
    longitude = (longitude - longitude.mean())

    # Calculate frequency domain
    freq = np.linspace(0.01, 10, 1000)
    pgram_latitude = lombscargle(time, latitude, freq, normalize=True)
    pgram_longitude = lombscargle(time, longitude, freq, normalize=True)

    #엑셀로 데이터 확인 합니다.
    #save_to_excel(combined_data, 'combined_data.xlsx')
    
    # 그래프를 그립니다.
    #plot_circadian_movement(time, latitude, longitude, pgram_latitude, pgram_longitude)


    ecm_latitude = compute_ECM(pgram_latitude)
    ecm_longitude = compute_ECM(pgram_longitude)
    weight_ecm_latitude = weight_compute_ECM(pgram_latitude)
    weight_ecm_longitude = weight_compute_ECM(pgram_longitude)

    # Output the dates used in the analysis along with ECM results
    # print('Dates used for analysis:', successful_dates)
    # print('Energy of Circadian Movement (Latitude) =', ecm_latitude)
    # print('Energy of Circadian Movement (Longitude) =', ecm_longitude)
    # print('Weight Circadian Movement (Latitude) =', weight_ecm_latitude)
    # print('Weight of Circadian Movement (Longitude) =', weight_ecm_longitude)

    return (weight_ecm_latitude + weight_ecm_longitude) / 2

#Example usage:
# result = circadianmovement_main(base_date, 'joowon@naver.com')
# if result != 0:
#     print(result)
