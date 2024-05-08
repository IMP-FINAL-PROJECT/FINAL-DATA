from collections import defaultdict

def calculate_scores(summary):
    for user, data in summary.items():
        data['score']['activity_score'] = calculate_activity_score(data['daytime']['pedometer'], data['sunset']['pedometer'])
        data['score']['phone_usage_frequency_score'] = calculate_phone_usage_frequency_score((data['daytime']['screen_frequency'] + (data['sunset']['screen_frequency'] * 2))/3)
        data['score']['phone_usage_duration_score'] = calculate_phone_usage_duration_score((data['daytime']['screen_duration'] + (data['sunset']['screen_duration'] * 2))/3)
        data['score']['call_duration_score'] = calculate_call_duration_score(data['daytime']['call_duration'], data['sunset']['call_duration'])
        daytime_illumination_score = calculate_day_illumination_score(data['daytime']['illuminance_avg'])
        night_illumination_score = calculate_night_illumination_score(data['sunset']['illuminance_avg'])
        data['score']['illumination_exposure_score'] = (daytime_illumination_score + night_illumination_score) / 2
        data['score']['location_diversity_score'] = calculate_location_diversity(data['gps']['cluster'])
        data['score']['homestay_score'] = calculate_homestay_score(data['gps']['homestay'])
        data['score']['sleeptime_screen_duration_score'] = calculate_sleeptime_screen_duration_score(data['sunset']['sleeptime_screen_duration'])

def calculate_location_diversity(clusters):
    num_clusters = len(clusters)
    max_clusters = 6
    min_clusters = 1
    if num_clusters >= max_clusters:
        return 100
    elif num_clusters <= min_clusters:
        return 0
    else:
        return (num_clusters - min_clusters) / (max_clusters - min_clusters) * 100

def calculate_activity_score(daytime_steps, sunset_steps):
    daily_target_steps = 10000 / 24
    average_steps_per_hour = (daytime_steps + sunset_steps)/2
    if average_steps_per_hour > daily_target_steps:
        return 100
    elif average_steps_per_hour <= 500:
        return 0
    else:
        return ((average_steps_per_hour - 500) / (daily_target_steps - 500)) * 100

def calculate_homestay_score(homestay_percentage):
    if homestay_percentage >= 1:
        return 100
    elif homestay_percentage > 0.5:
        return (homestay_percentage - 0.5) * 200
    else:
        return 0

def calculate_phone_usage_frequency_score(frequency):
    max_score = 100
    max_frequency = 60
    if frequency >= max_frequency:
        return 100
    else:
        return (frequency / max_frequency) * max_score

def calculate_phone_usage_duration_score(duration):
    max_duration = 15 * 60 * 1000
    if duration >= max_duration:
        return 100
    else:
        return (duration / max_duration) * 100

def calculate_day_illumination_score(illuminance):
    max_illuminance = 800
    min_illuminance = 100
    if illuminance >= max_illuminance:
        return 100
    elif illuminance <= min_illuminance:
        return 0
    else:
        return (illuminance - min_illuminance) / (max_illuminance - min_illuminance) * 100

def calculate_night_illumination_score(illuminance):
    max_illuminance = 200
    min_illuminance = 40
    if illuminance > max_illuminance:
        return 0
    elif illuminance <= min_illuminance:
        return 100
    else:
        return 100 - ((illuminance - min_illuminance) / (max_illuminance - min_illuminance) * 100)

def calculate_call_duration_score(daytime_duration, sunset_duration):
    average_call_duration = (daytime_duration + sunset_duration) / 2
    max_call_duration = 10000
    if average_call_duration >= max_call_duration:
        return 100
    elif average_call_duration == 0:
        return 0
    else:
        return (average_call_duration / max_call_duration) * 100

def calculate_sleeptime_screen_duration_score(sleeptime_screen_duration):
    max_duration = 60 * 60 * 1000
    if sleeptime_screen_duration >= max_duration:
        return 100
    else:
        return (sleeptime_screen_duration / max_duration) * 100
