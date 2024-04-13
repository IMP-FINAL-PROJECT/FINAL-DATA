import folium

def create_and_save_map(gps_data, id, date):
    if not gps_data:
        return None

    # 맵의 중심을 첫 번째 GPS 데이터의 위치로 설정
    map_center = gps_data[0][:2]
    map_object = folium.Map(location=map_center, zoom_start=15)

    # 모든 GPS 좌표를 연결하는 선을 그리고, 각 위치에 마커를 추가
    for i in range(len(gps_data) - 1):
        current_coords = gps_data[i][:2]
        next_coords = gps_data[i + 1][:2]
        # 라인 추가
        folium.PolyLine(locations=[current_coords, next_coords], color='blue').add_to(map_object)
        # 마커 추가: 머문 시간과 타임스탬프를 팝업에 표시
        folium.Marker(
            location=current_coords, 
            popup=f'머문 시간: {gps_data[i][2]/1000} 초<br>시간: {gps_data[i][3]}'
        ).add_to(map_object)
    
    # 마지막 위치에 마커 추가
    folium.Marker(
        location=gps_data[-1][:2], 
        popup=f'머문 시간: {gps_data[-1][2]/1000} 초<br>시간: {gps_data[-1][3]}'
    ).add_to(map_object)
    
    # 결과 맵 파일 저장
    map_file_path = f"./gps_map/{id}_{date}_MAP.html"
    map_object.save(map_file_path)
    return map_file_path
