from collections import defaultdict

def classify_data_by_id(sensor_data_list):
    data_by_id = defaultdict(list)
    for data in sensor_data_list:
        data_by_id[data[1]].append(data)
    return data_by_id


