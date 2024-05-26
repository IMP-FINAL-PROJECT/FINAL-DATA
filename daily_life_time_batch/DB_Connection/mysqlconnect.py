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

def execute_val_query(query,val):
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
            cursor.execute(query,val)  # 쿼리 실행
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




def execute_insert_query(query):
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
            conn.commit()
    finally:
        conn.close()  # 데이터베이스 연결 종료     

def excutemany_delete_query(query,val_list):
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
            # existing_entries_list 순회
            for id, date in val_list:
                # DELETE 쿼리 실행
                cursor.execute(query, (id, date))
                print(query)
            # 변경 사항 저장
            conn.commit()

    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()  # 오류 발생 시 롤백

    finally:
        conn.close()  # 연결 닫기

