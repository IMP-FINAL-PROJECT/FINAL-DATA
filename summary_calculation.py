
def calculate_averages(summary):
    """각 카테고리별로 평균값을 계산하는 래퍼 함수입니다."""
    for categories in summary.values():
        for category in ['daytime', 'sunset']:
            if categories[category]['count'] > 0:
                calculate_illuminance_avg(categories, category)
                calculate_pedometer_avg(categories, category)
                calculate_screen_frequency_avg(categories, category)
                calculate_screen_duration_avg(categories, category)


def calculate_illuminance_avg(categories, category):
    """'illuminance_avg'의 평균값을 계산합니다."""
    categories[category]['illuminance_avg'] = categories[category]['illuminance_sum'] / categories[category]['count']
    del categories[category]['illuminance_sum']  # 사용 완료된 합계 값 삭제

def calculate_pedometer_avg(categories, category):
    """'pedometer'의 평균값을 계산합니다."""
    categories[category]['pedometer'] /= categories[category]['count']

def calculate_screen_frequency_avg(categories, category):
    """'screen_frequency'의 평균값을 계산합니다."""
    categories[category]['screen_frequency'] /= categories[category]['count']

def calculate_screen_duration_avg(categories, category):
    """'screen_duration'의 평균값을 계산합니다."""
    categories[category]['screen_duration'] /= categories[category]['count']
