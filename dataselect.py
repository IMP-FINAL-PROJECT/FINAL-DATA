import mysqlconnect


# 데이터베이스에서 id와 date 조합 쿼리
def query_existing_id_date_combinations():

    query = "SELECT id, date FROM daily_life_pattern"
    result = mysqlconnect.execute_query(query)
    
    return [(row[0], str(row[1])) for row in result]      # id와 date 조합을 튜플 형태로 저장
