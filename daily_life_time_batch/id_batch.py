import DB_Connection.mysqlconnect as mysqlconnect

# 사용자 데이터를 조회
user_data_query = "SELECT id FROM user"
user_data = mysqlconnect.execute_query(user_data_query)

# 현재 batch_id 테이블의 id 조회
id_data_query = "SELECT id FROM batch_id"
id_data = mysqlconnect.execute_query(id_data_query)

# user_data와 id_data에서 id만 추출하여 set으로 변환
user_ids = {row[0] for row in user_data}
batch_ids = {row[0] for row in id_data}

# user_ids에서 batch_ids를 제외한 새로 삽입할 데이터 계산
new_ids = user_ids - batch_ids
new_data = [(id,) for id in new_ids]  # executemany에 적합한 형태로 변환

# 새로운 데이터가 있다면 데이터베이스에 삽입
if new_data:
    mysqlconnect.executemany_query('INSERT INTO batch_id (id) VALUES (%s)', new_data)
    print(f"Inserted {len(new_data)} new IDs.")
else:
    print("No new IDs to insert.")
