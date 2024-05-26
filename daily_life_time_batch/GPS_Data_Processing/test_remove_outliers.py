import json
import numpy as np
import folium
import os
from datetime import datetime
import math
from selenium import webdriver
from PIL import Image
import imageio
import time

# 파일에서 데이터 로드
def load_data(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    gps_data = sorted([[float(item[0]), float(item[1]), float(item[2]), datetime.fromisoformat(item[3])] for item in data], key=lambda x: x[3])
    return gps_data

# 이상치 제거 함수
def remove_outliers(gps_data, driver):
    i = 1
    threshold = 0.0001
    last_removed_index = -1
    frame_num = 0  # Initialize frame counter

    while i < len(gps_data) - 1:
        if last_removed_index != -1:
            prev = last_removed_index
        else:
            prev = gps_data[i - 1]
        
        curr = gps_data[i]
        next = gps_data[i + 1]
        
        avg_lat = (prev[0] + next[0]) / 2
        avg_lon = (prev[1] + next[1]) / 2
        
        distance = math.sqrt((curr[0] - avg_lat)**2 + (curr[1] - avg_lon)**2)
        
        if distance > threshold:
            gps_data[i - 1][2] += curr[2]
            gps_data.pop(i)
            last_removed_index = curr
            update_map(gps_data, frame_num, driver)  # Save frame only if outlier is removed
            frame_num += 1
        else:
            last_removed_index = -1
            threshold = 0.0001
            i += 1

    return gps_data

# 지도 업데이트 및 이미지 저장 함수
def update_map(gps_data, frame_num, driver):
    m = folium.Map(location=[np.mean([pt[0] for pt in gps_data]), np.mean([pt[1] for pt in gps_data])], zoom_start=15)
    
    for pt in gps_data:
        folium.CircleMarker(location=[pt[0], pt[1]], radius=5, color='blue', fill=True).add_to(m)
    
    output_path = f'map_frames/frame_{frame_num:03d}.png'
    m.save('map.html')

    # Convert HTML to PNG using selenium and save
    driver.get(f'file://{os.path.abspath("map.html")}')
    time.sleep(2)  # Allow map to load
    driver.save_screenshot(output_path)

# 애니메이션 생성 함수
def create_outlier_removal_animation(original_gps_data):
    if not os.path.exists('map_frames'):
        os.makedirs('map_frames')
    
    # Set up the Selenium web driver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    
    gps_data = [list(item) for item in original_gps_data]
    
    gps_data = remove_outliers(gps_data, driver)
    
    driver.quit()
    
    # 이미지 파일들을 애니메이션으로 결합
    images = []
    for filename in sorted(os.listdir('map_frames')):
        if filename.endswith('.png'):
            images.append(imageio.imread(os.path.join('map_frames', filename)))
    
    imageio.mimsave('outlier_removal_animation.gif', images, duration=200)  # FPS를 5로 설정하기 위해 duration을 200ms로 설정

# 메인 실행
file_path = "./gps_data/2024-04-04/dongwook@naver.com.json"
gps_data = load_data(file_path)
create_outlier_removal_animation(gps_data)
