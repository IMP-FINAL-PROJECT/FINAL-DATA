import json
import os

def save_gps_data(gps_data, id, date):
    # 경로 설정: 'gps_data' 폴더 내 날짜별 서브폴더
    directory = f"./gps_data/{date}"
    if not os.path.exists(directory):
        os.makedirs(directory)  # 해당 경로가 없으면 생성

    # 파일 경로 설정: ID를 파일 이름으로 사용
    file_path = os.path.join(directory, f"{id}.json")
    
    # 데이터를 JSON 파일로 저장
    with open(file_path, 'w') as file:
        json.dump(gps_data, file, indent=4)

    return file_path
