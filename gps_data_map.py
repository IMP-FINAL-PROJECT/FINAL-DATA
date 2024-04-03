import folium


#데이터를 
def create_and_save_map(gps_data, id, date):
    if not gps_data:
        return None

    map_center = gps_data[0][:2]
    map_object = folium.Map(location=map_center, zoom_start=15)

    for i in range(len(gps_data) - 1):
        current_coords = gps_data[i][:2]
        next_coords = gps_data[i + 1][:2]
        folium.PolyLine(locations=[current_coords, next_coords], color='blue').add_to(map_object)
        folium.Marker(location=current_coords, popup=f'머문 시간: {gps_data[i][2]/1000} 초').add_to(map_object)
    
    folium.Marker(location=gps_data[-1][:2], popup=f'머문 시간: {gps_data[-1][2]/1000} 초').add_to(map_object)
    
    map_file_path = f"./gps_map/{id}_{date}_MAP.html"
    map_object.save(map_file_path)
    return map_file_path
