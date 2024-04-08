import pymysql
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

# 연결 설정  

# MySQL 데이터베이스 연결 및 쿼리 실행 함수
def execute_query(query):
    conn = pymysql.connect(
        host=os.environ.get("Server_IP"),            # MySQL 서버 주소
        user=os.environ.get("MYSQL_USER"),           # MySQL 사용자 이름
        password=os.environ.get("MYSQL_PASSWORD"),   # MySQL 사용자 비밀번호
        db='final',                                  # 접속할 데이터베이스 이름
        charset='utf8mb4',                           # 문자 인코딩 설정
        port=3306                                    # 포트 번호
    )

    
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)  # 쿼리 실행
            result = cursor.fetchall()  # 모든 결과 행 가져오기
            return result  # 결과 반환
    finally:
        conn.close()  # 데이터베이스 연결 종료


def executemany_query(query,val):
    conn = pymysql.connect(
        host=os.environ.get("Server_IP"),            # MySQL 서버 주소
        user=os.environ.get("MYSQL_USER"),           # MySQL 사용자 이름
        password=os.environ.get("MYSQL_PASSWORD"),   # MySQL 사용자 비밀번호
        db='final',                                  # 접속할 데이터베이스 이름
        charset='utf8mb4',                           # 문자 인코딩 설정
        port=3306                                    # 포트 번호
    )

    
    try:
        with conn.cursor() as cursor:
            cursor.executemany(query,val)  # 쿼리 실행
            conn.commit()
    finally:
        conn.close()  # 데이터베이스 연결 종료

