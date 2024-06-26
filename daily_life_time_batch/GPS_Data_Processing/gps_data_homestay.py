import math
from Data_Manage.data_select import fetch_gps_home_data
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
        stay_ratio, cluster_lat, cluster_lon = cluster
        distance = haversine(home_lat, home_lon, cluster_lat, cluster_lon)
        
        if distance <= 50:  # 50미터 이내인 경우
            return stay_ratio  # 해당 클러스터의 머문 비율 반환
    
    # 반경 50미터 내에 클러스터가 없는 경우
    return 0


def homestay_percentage(id, clustering_results):
    # 데이터베이스에서 id에 해당하는 데이터를 가져옴
    result = fetch_gps_home_data(id)
    
    # 결과가 비어있지 않은지 확인
    if result and result[0]:  # result가 비어있지 않고, result의 첫 번째 요소도 비어있지 않을 때
        gps_data_str = result[0][0]  # 문자열 데이터 추출
        gps_data = literal_eval(gps_data_str)  # 문자열을 리스트로 변환
        print(id)
        # 예시 위도 경도 (집의 위도, 경도)
        home_lat, home_lon = gps_data
        
        # 집 근처 클러스터의 머문 비율 반환
        return check_stay_ratio(clustering_results, home_lat, home_lon)
    else:
        # 유효한 데이터가 없는 경우, 적절한 오류 메시지나 기본값 반환
        return -1
