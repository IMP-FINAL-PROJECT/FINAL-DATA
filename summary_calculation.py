
#각 데이터 별로 카운트에 따라 평균을 계산하는 함수
def calculate_averages(summary):
    for categories in summary.values():
        for category in ['daytime', 'sunset']:
            if categories[category]['count'] > 0:
                categories[category]['illuminance_avg'] = categories[category]['illuminance_sum'] / categories[category]['count']
                categories[category]['pedometer'] /= categories[category]['count']
                categories[category]['screen_frequency'] /= categories[category]['count']
                categories[category]['screen_duration'] /= categories[category]['count']
                del categories[category]['illuminance_sum']  # 중간 합산값 삭제
