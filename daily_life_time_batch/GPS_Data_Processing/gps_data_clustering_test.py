import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from sklearn.cluster import DBSCAN, KMeans
from sklearn.preprocessing import StandardScaler
from datetime import datetime

# 파일에서 데이터 로드
def load_data(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    # 타임스탬프를 포함하여 데이터 로드, 타임스탬프로 정렬
    gps_data = sorted([(float(item[0]), float(item[1]), float(item[2]), datetime.fromisoformat(item[3])) for item in data], key=lambda x: x[3])
    return np.array(gps_data)

# 데이터 필터링 및 복제
def preprocess_data(gps_data):
    # 1분 이상 머무른 데이터만 필터링
    filtered_data = [data for data in gps_data if data[2] >= 60000]
    move_data = [data[:2] for data in gps_data if data[2] < 60000]  # 머무른 시간이 1분 미만인 데이터

    # 머무른 시간에 비례하여 데이터 복제
    weighted_data = []
    for data in filtered_data:
        latitude, longitude, duration = data[:3]
        copies = duration // 60000  # 1분 단위로 복제
        for _ in range(int(copies)):
            weighted_data.append([latitude, longitude])

    return np.array(weighted_data), np.array(move_data)

# 클러스터링 함수
def cluster_data(method, data):
    if method == 'DBSCAN':
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(data)
        dbscan = DBSCAN(eps=0.3, min_samples=5)
        dbscan.fit(scaled_data)
        return dbscan.labels_, data
    elif method == 'KMeans':
        kmeans = KMeans(n_clusters=3, random_state=0)
        kmeans.fit(data)
        return kmeans.labels_, data
    else:  # 위치 분산 클러스터링 (예시)
        mean_lat = np.mean(data[:, 0])
        mean_long = np.mean(data[:, 1])
        return np.array([0 if (x - mean_lat)**2 + (y - mean_long)**2 < 25 else 1 for x, y in data]), data

# 원의 반지름 계산 함수
def calculate_radius(data, labels, cluster_index):
    cluster_points = data[labels == cluster_index]
    centroid = np.mean(cluster_points, axis=0)
    radius = np.max(np.sqrt(np.sum((cluster_points - centroid) ** 2, axis=1)))
    return radius

# 시각화 및 비디오 생성
def create_video(gps_data, processed_data, move_data):
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    methods = ['DBSCAN', 'KMeans', 'Position Variance']
    colors = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta']

    def init():
        for ax in axs:
            ax.set_xlim(np.min(gps_data[:, 0]) - 0.01, np.max(gps_data[:, 0]) + 0.01)
            ax.set_ylim(np.min(gps_data[:, 1]) - 0.01, np.max(gps_data[:, 1]) + 0.01)
        return axs

    def update(frame):
        for ax, method in zip(axs, methods):
            ax.clear()
            labels, data = cluster_data(method, processed_data)
            unique_labels = set(labels)
            for k in unique_labels:
                if k != -1:
                    class_member_mask = (labels == k)
                    xy = data[class_member_mask]
                    ax.scatter(xy[:, 0], xy[:, 1], color=colors[k % len(colors)], label=f'Cluster {k}')
                    center = np.mean(xy, axis=0)
                    radius = calculate_radius(data, labels, k)
                    ax.add_patch(plt.Circle(center, radius, color=colors[k % len(colors)], fill=False, linewidth=2))
            ax.scatter(move_data[:, 0], move_data[:, 1], color='gray', marker='x', label='Move Data')
            current_point = gps_data[frame]
            ax.plot(current_point[0], current_point[1], 'o', color='red', markersize=10)
            ax.set_title(f"{method} Clustering: {current_point[3].strftime('%Y-%m-%d %H:%M:%S')}")
            ax.legend()

        return axs

    ani = animation.FuncAnimation(fig, update, frames=len(gps_data), init_func=init, blit=False, interval=50)
    ani.save('clustering_with_timestamps.mp4', writer='ffmpeg', fps=20)

# 메인 실행
file_path = "./gps_data/2024-04-24/joowon@naver.com.json"
gps_data = load_data(file_path)
processed_data, move_data = preprocess_data(gps_data[:, :3])
create_video(gps_data, processed_data, move_data)
