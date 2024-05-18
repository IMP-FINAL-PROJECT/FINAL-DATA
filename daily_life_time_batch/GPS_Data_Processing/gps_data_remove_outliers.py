import math

def remove_outliers(gps_data):
    i = 1  # 첫 번째와 마지막 데이터는 비교 대상이 없으므로 중간 데이터부터 시작
    threshold = 0.0005  # 초기 이상치 판단 기준
    last_removed_index = -1  # 마지막으로 제거된 이상치의 인덱스 초기화
    
    while i < len(gps_data) - 1:
        # 제거된 이상치를 고려하여 이전 위치 결정
        if last_removed_index !=  -1:
            prev = last_removed_index  # 이상치가 제거된 위치
        else:
            prev = gps_data[i - 1]
        
        curr = gps_data[i]
        next = gps_data[i + 1]
        
        # 전후 데이터의 평균 위치 계산
        avg_lat = (prev[0] + next[0]) / 2
        avg_lon = (prev[1] + next[1]) / 2
        
        # 현재 위치와 평균 위치 사이의 거리 계산
        distance = math.sqrt((curr[0] - avg_lat)**2 + (curr[1] - avg_lon)**2)
        
        # 거리가 현재 threshold 이상 차이 나면 이상치로 간주
        if distance > threshold:
            gps_data[i - 1][2] += curr[2]  # 이전 데이터에 이상치 duration 추가
            gps_data.pop(i)  # 이상치 삭제
            last_removed_index = curr  # 마지막으로 이상치가 제거된 위치 저장
            print("이상치 제거: 위치 = ({}, {}), 새 기준 = {}".format(curr[0], curr[1], threshold))
        else:
            last_removed_index = -1  # 이상치가 아니면 리셋
            threshold = 0.0005  # 이상치 아니면 기준 리셋
            i += 1

    return gps_data