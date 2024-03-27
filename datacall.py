import mysqlconnect

def get_latest_start_num():
    """
    데이터베이스에서 가장 큰 start_num 값을 가져오는 함수
    """
    batch_num_query = "SELECT start_num FROM batch ORDER BY start_num DESC LIMIT 1"
    result = mysqlconnect.execute_query(batch_num_query)
    # result에서 첫 번째 행, 첫 번째 열의 값을 가져옴
    print(result[0][0])
    if result:
        return result[0][0]
    else:
        return None
