import numpy as np
from sklearn.cluster import DBSCAN
from collections import Counter

def perform_dbscan_clustering(gps_data):

    if not gps_data:
        return []
    # 1분 이상 머무른 데이터만 필터링 (1분 = 60000ms)
    filtered_data = [data for data in gps_data if data[2] >= 60000]

    # 머무른 시간에 비례하여 데이터 복제 (1분마다 1회 복제)
    weighted_data = []
    for data in filtered_data:
        latitude, longitude, duration,timestamp = data
        copies = duration // 60000  # 1분 단위로 복제
        for _ in range(int(copies)):
            weighted_data.append([latitude, longitude])

    cluster_info = []

    if weighted_data:
        weighted_data = np.array(weighted_data)
        dbscan = DBSCAN(eps=0.001, min_samples=5)
        dbscan.fit(weighted_data)

        labels = dbscan.labels_
        clusters = np.unique(labels[labels != -1])  # 잡음 데이터 제외

        if clusters.size > 0:
            cluster_counts = Counter(labels)
            total_points = len(weighted_data[labels != -1])

            for cluster in clusters:
                points = weighted_data[labels == cluster]
                center = points.mean(axis=0)
                ratio = cluster_counts[cluster] / total_points
                cluster_info.append([ratio, center[0] ,center[1]])
    cluster_info = sorted(cluster_info, key=lambda x: x[0], reverse=True)
    return cluster_info
