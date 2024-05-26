import pandas as pd
import math
# Load the Excel file to see its structure
Sunrise_and_Sunset_file_path = 'DATA/Sunrise_and_Sunset/Sunrise_and_Sunset_excel.xlsx'
Sunrise_and_Sunset_data = pd.read_excel(Sunrise_and_Sunset_file_path)

# Display the first few rows of the dataframe to understand its structure
Sunrise_and_Sunset_data.head()


def get_sunrise_sunset(date):
    """
    Returns the sunrise and sunset times for a given date in MMDD format.

    Parameters:
    date (str): The date in MMDD format.

    Returns:
    tuple: Sunrise and sunset times or a message if the date is not found.
    """
    # Convert the date input to int for comparison
    date_int = int(date)
    
    # Check if the date is in the DataFrame
    if date_int in Sunrise_and_Sunset_data['날짜'].values:
        sunrise, sunset = Sunrise_and_Sunset_data[Sunrise_and_Sunset_data['날짜'] == date_int][['출', '몰']].iloc[0]
        return (sunrise, sunset)
    else:
        return ("No data available for the given date.",)


def round_up_time(time_str):
    """
    Rounds up the given time to the nearest hour.

    Parameters:
    time_str (str): The time string in HH:MM format.

    Returns:
    int: The rounded up hour.
    """
    # 시간과 분으로 분리
    hour, minute = map(int, time_str.split(':'))
    
    # 분이 0보다 크면 시간을 1 증가시켜 올림 처리
    if minute > 0:
        hour += 1
    
    # 24시간 형식을 유지하기 위해 24로 나눈 나머지를 반환
    return hour % 24

# 예시 사용법
# sunrise = "07:30"
# sunset = "18:45"
# rounded_sunrise = round_up_time(sunrise)
# rounded_sunset = round_up_time(sunset)
# print(rounded_sunrise, rounded_sunset)  # 출력 예: 8 19