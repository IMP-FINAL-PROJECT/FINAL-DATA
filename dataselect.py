import mysqlconnect
from datetime import timedelta

# 데이터베이스에서 id와 date 조합 쿼리
def query_existing_id_date_combinations():

    query = "SELECT id, date FROM daily_life_pattern"
    result = mysqlconnect.execute_query(query)

    return [(row[0], str(row[1])) for row in result]      # id와 date 조합을 튜플 형태로 저장


def fetch_data_from_db(data_to_fetch, batch_sensor_data_start_num):
    results = []

    for id, sunrise_today, sunrise_next_day, date in data_to_fetch:
        query = """
        SELECT * FROM sensor
        WHERE id = %s AND ((timestamp = %s AND hour >= %s) OR (timestamp = %s AND hour < %s)) AND number < %s;
        """
        print(batch_sensor_data_start_num)
        results+=mysqlconnect.execute_val_query(query, (id, date, sunrise_today, (date + timedelta(days=1)), sunrise_next_day, batch_sensor_data_start_num))
    return results
