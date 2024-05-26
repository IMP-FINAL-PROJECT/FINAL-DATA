import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.signal import lombscargle

# Global parameters
no_of_past_days = 5
hours_a_day = 144
select_circadianmovement = [100, 200, 300, 400, 600, 800, 1200, 2400]
weight_circadianmovement = [8, 7, 6, 5, 4, 3, 2, 1]
margin_window = 30

def compute_ECM(data, margin_window_begin=70, margin_window_end=130):
    result = sum(data[margin_window_begin:margin_window_end])
    return result

def weight_compute_ECM(data):
    result = 0
    for i in select_circadianmovement:
        result += sum(data[i - margin_window:i + margin_window]) * weight_circadianmovement[select_circadianmovement.index(i)]
    return result / sum(weight_circadianmovement)

def create_regular_intervals(data, interval_seconds=int(86400 / hours_a_day)):
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

    if len(df) < hours_a_day * 0.7:
        return

    df = df.resample(f'{interval_seconds}s').mean().interpolate()
    return df

def generate_file_paths(base_date, days, id):
    if isinstance(base_date, str):
        base_date = datetime.fromisoformat(base_date)
    file_paths = []
    for i in range(days):
        date = base_date - timedelta(days=days - 1 - i)
        file_path = f'./gps_data/{date.strftime("%Y-%m-%d")}/{id}.json'
        file_paths.insert(0, file_path)
    return file_paths

def load_and_process_gps_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return create_regular_intervals(data)
    except FileNotFoundError:
        return

def circadianmovement_main(base_date, id):
    file_paths = generate_file_paths(base_date, no_of_past_days * 2, id)
    successful_dates = []
    dataframes = []
    for file_path in file_paths:
        df = load_and_process_gps_data(file_path)
        if df is not None:
            dataframes.append(df)
            date_from_path = file_path.split('/')[-2]
            successful_dates.append(date_from_path)

    if len(dataframes) < no_of_past_days:
        print("Insufficient data to perform analysis. Returning 0.")
        return 0

    dataframes = dataframes[:no_of_past_days]
    successful_dates = successful_dates[:no_of_past_days]

    dataframes.reverse()
    successful_dates.reverse()

    combined_data = pd.concat(dataframes)
    combined_data.reset_index(inplace=True)

    required_samples = no_of_past_days * hours_a_day
    if len(combined_data) < required_samples:
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
    
    time = np.linspace(0, no_of_past_days * (2 * np.pi), required_samples)
    latitude = combined_data['latitude'].values
    longitude = combined_data['longitude'].values

    latitude = (latitude - latitude.mean())
    longitude = (longitude - longitude.mean())

    freq = np.linspace(0.01, 10, 1000)
    pgram_latitude = lombscargle(time, latitude, freq, normalize=True)
    pgram_longitude = lombscargle(time, longitude, freq, normalize=True)

    fig, axs = plt.subplots(4, 1, figsize=(10, 12), constrained_layout=True)
    axs[0].set_title('Time-Domain Plot (Latitude)')
    axs[1].set_title('Lomb-Scargle Periodogram (Latitude)')
    axs[2].set_title('Time-Domain Plot (Longitude)')
    axs[3].set_title('Lomb-Scargle Periodogram (Longitude)')

    def update(frame):
        axs[0].plot(time[:frame], latitude[:frame], 'bo')
        axs[1].plot(freq[:frame], pgram_latitude[:frame], 'b-')
        axs[2].plot(time[:frame], longitude[:frame], 'go')
        axs[3].plot(freq[:frame], pgram_longitude[:frame], 'g-')

    ani = FuncAnimation(fig, update, frames=required_samples, interval=200)
    ani.save(f'{id}_circadian_movement.mp4', writer='ffmpeg', fps=5)

# Example usage:
result = circadianmovement_main('2024-04-24', 'joowon@naver.com')
if result != 0:
    print(result)
