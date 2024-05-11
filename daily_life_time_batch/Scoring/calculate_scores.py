from collections import defaultdict
import configparser

# 설정 파일 불러오기
config = configparser.ConfigParser()
config.read('config.ini')

max_score = int(config['score']['max_score'])
min_score = int(config['score']['min_score'])


def calculate_activity_score(daytime_steps, sunset_steps):
    daily_max_target_steps = int(config['score']['daily_max_step']) / 24
    daily_min_target_steps = int(config['score']['daily_min_step']) / 24
    average_steps_per_hour = (daytime_steps + sunset_steps) / 2
    if average_steps_per_hour > daily_max_target_steps:
        return max_score
    elif average_steps_per_hour <= daily_min_target_steps:
        return 0
    else:
        return ((average_steps_per_hour - daily_min_target_steps) / (daily_max_target_steps - daily_min_target_steps)) * max_score

def calculate_homestay_score(homestay_percentage):
    daily_min_homestay = float(config['score']['daily_min_homestay'])
    if homestay_percentage >= daily_min_homestay:
        return 0
    elif homestay_percentage > float(config['score']['daily_max_homestay']):
        return (1 - homestay_percentage) * max_score * daily_min_homestay / float(config['score']['daily_max_homestay'])
    else:
        return max_score

def calculate_phone_usage_frequency_score(frequency):
    max_frequency = int(config['score']['max_frequency'])
    if frequency >= max_frequency:
        return max_score
    else:
        return (frequency / max_frequency) * max_score

def calculate_phone_usage_duration_score(duration):
    max_duration = int(config['score']['max_duration']) * 60000  # 분에서 밀리초로 변환
    min_duration = int(config['score']['min_duration']) * 60000  # 분에서 밀리초로 변환
   
    if duration <= min_duration:
        return max_score  # 최소 사용 시간 이하일 경우 최대 점수
    elif duration >= max_duration:
        return min_score  # 최대 사용 시간 초과일 경우 최소 점수
    else:
        # 사용 시간이 최소와 최대 사이일 경우 선형적으로 점수 계산
        return max_score - ((duration - min_duration) / (max_duration - min_duration) * (max_score - min_score))

def calculate_day_illumination_score(illuminance):
    max_illuminance = int(config['score']['max_illuminance'])
    min_illuminance = int(config['score']['min_illuminance'])
    if illuminance >= max_illuminance:
        return max_score
    elif illuminance <= min_illuminance:
        return min_score
    else:
        return (illuminance - min_illuminance) / (max_illuminance - min_illuminance) * max_score

def calculate_night_illumination_score(illuminance):
    max_illuminance = int(config['score']['max_night_illuminance'])
    min_illuminance = int(config['score']['min_night_illuminance'])
    if illuminance > max_illuminance:
        return min_score
    elif illuminance <= min_illuminance:
        return max_score
    else:
        return max_score - ((illuminance - min_illuminance) / (max_illuminance - min_illuminance) * max_score)

def calculate_call_duration_score(daytime_duration, sunset_duration):
    max_call_duration = int(config['score']['max_call_duration'])
    average_call_duration = (daytime_duration + sunset_duration) / 2
    if average_call_duration >= max_call_duration:
        return max_score
    elif average_call_duration == 0:
        return 0
    else:
        return (average_call_duration / max_call_duration) * max_score

def calculate_sleeptime_screen_duration_score(sleeptime_screen_duration):
    max_duration = int(config['score']['sleeptime_max_duration'])
    if sleeptime_screen_duration >= max_duration:
        return max_score
    else:
        return (sleeptime_screen_duration / max_duration) *max_score

def calculate_location_diversity(clusters):
    num_clusters = len(clusters)
    max_clusters = int(config['score']['max_clusters'])
    min_clusters = int(config['score']['min_clusters'])
    if num_clusters >= max_clusters:
        return max_score
    elif num_clusters <= min_clusters:
        return int(config['score']['min_score'])
    else:
        return (num_clusters - min_clusters) / (max_clusters - min_clusters) * max_score

def calculate_scores(summary):
    for user, data in summary.items():
        data['score'] = {}
        data['score']['activity_score'] = calculate_activity_score(data['daytime']['pedometer'], data['sunset']['pedometer'])
        data['score']['phone_usage_score'] = (calculate_phone_usage_frequency_score((data['daytime']['screen_frequency'] + data['sunset']['screen_frequency'] * 2)/3) +
                                             calculate_phone_usage_duration_score((data['daytime']['screen_duration'] + data['sunset']['screen_duration'] * 2)/3) +
                                             calculate_sleeptime_screen_duration_score(data['sunset']['sleeptime_screen_duration'])) / 3
        data['score']['illumination_exposure_score'] = (calculate_day_illumination_score(data['daytime']['illuminance_avg']) +
                                                       calculate_night_illumination_score(data['sunset']['illuminance_avg'])) / 2
        data['score']['location_diversity_score'] = (calculate_location_diversity(data['gps']['cluster']) +
                                                     calculate_homestay_score(data['gps']['homestay'])) / 2
        data['score']['circadian_rhythm_score'] = data['gps']['life_routine_consistency']