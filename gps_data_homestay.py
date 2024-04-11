import math
from dataselect import fetch_gps_home_data
from ast import literal_eval
def haversine(lat1, lon1, lat2, lon2):
    # 지구 반지름 (미터)
    R = 6371000
    
    # 라디안으로 변환
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    # 허버사인 공식 사용
    a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    # 총 거리 (미터 단위)
    distance = R * c
    return distance

def check_stay_ratio(clustering_results, home_lat, home_lon):
    for cluster in clustering_results:
        cluster_id, stay_ratio, cluster_lat, cluster_lon = cluster
        distance = haversine(home_lat, home_lon, cluster_lat, cluster_lon)
        
        if distance <= 50:  # 50미터 이내인 경우
            return stay_ratio  # 해당 클러스터의 머문 비율 반환
    
    # 반경 50미터 내에 클러스터가 없는 경우
    return 0

def homestay_percentage(id,clustering_results):
    # 데이터베이스에서 id에 해당하는 데이터를 가져옴
    gps_data = literal_eval((fetch_gps_home_data(id))[0][0])
    # 예시 위도 경도 (집의 위도, 경도)
    home_lat = gps_data[0]
    home_lon = gps_data[1]
    # 집 근처 클러스터의 머문 비율 반환
    return check_stay_ratio(clustering_results, home_lat, home_lon)

clustering_results = [[0, 0.8933739527798934, 36.79894089759768, 127.0804083873752], [1, 0.10662604722010663, 36.79354076385498, 127.08188258579798]]


print(homestay_percentage("dongwook@naver.com",clustering_results))
