import pymysql
from dotenv import load_dotenv
import os


load_dotenv()
# MySQL 데이터베이스 연결 설정
conn = pymysql.connect(
    host=os.environ.get("Server_IP"),    # MySQL 서버 주소
    user=os.environ.get("MYSQL_USER"),    # MySQL 사용자 이름
    password=os.environ.get("MYSQL_PASSWORD"),  # MySQL 사용자 비밀번호
    db='final',        # 접속할 데이터베이스 이름
    charset='utf8mb4',    # 문자 인코딩 설정 
    port=3306,    # 포트 번호
)

try:
    # 커서 생성
    with conn.cursor() as cursor:
        # SQL 쿼리 실행
        sql = "SELECT * FROM user"  # 데이터를 가져올 테이블의 이름을 'your_table' 대신 사용
        cursor.execute(sql)

        # 결과 가져오기
        result = cursor.fetchall()
        for row in result:
            print(row)  # 각 행의 데이터 출력

finally:
    # 데이터베이스 연결 종료
    conn.close()
