import pandas as pd

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

# Test the function with a date from the dataset and a date not in the dataset
test_date_valid = '0102'  # A valid date in the dataset
test_date_invalid = '1231'  # An invalid date, assuming not in the dataset

print(get_sunrise_sunset(test_date_valid), get_sunrise_sunset(test_date_invalid))
