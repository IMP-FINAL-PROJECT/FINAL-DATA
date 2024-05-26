# 데이터베이스 연결을 위해 필요한 모듈과 구성 파일을 임포트합니다.
import DB_Connection.mysqlconnect as mysqlconnect
from .config import LATEST_START_NUM_QUERY, SENSOR_DATA_QUERY_TEMPLATE

def get_latest_start_num():
    """
    사전 정의된 SQL 쿼리를 사용하여 데이터베이스에서 가장 큰 start_num 값을 가져옵니다.
    이 함수는 batch 테이블에서 가장 최근의 start_num을 찾아 그 값을 반환합니다.
    반환값은 데이터 처리를 위한 시작점으로 사용됩니다.
    """
    # 사전 정의된 쿼리를 실행합니다.
    result = mysqlconnect.execute_query(LATEST_START_NUM_QUERY)
    # 결과가 존재하면 첫 번째 요소를 반환합니다. 결과가 없다면 None을 반환합니다.
    if result:
        return result[0][0]
    else:
        return None
    

def get_sensor_data(start_num):
    """
    제공된 start_num 이상의 번호를 가진 센서 테이블의 모든 레코드를 사전 정의된 SQL 템플릿을 사용하여 검색합니다.
    이 함수는 주어진 start_num을 기준으로 센서 데이터를 조회하고, 해당 데이터를 리스트 형태로 반환합니다.
    이 데이터는 분석이나 다른 처리 과정에 사용될 수 있습니다.
    """
    # 사전 정의된 SQL 템플릿에 start_num을 적용하여 쿼리를 완성합니다.
    sensor_data_query = SENSOR_DATA_QUERY_TEMPLATE.format(start_num)
    # 쿼리를 실행하고 결과 데이터를 반환합니다.
    sensor_data = mysqlconnect.execute_query(sensor_data_query)
    return sensor_data
