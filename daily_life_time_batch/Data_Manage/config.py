import configparser

# 설정 파일을 읽기 위한 ConfigParser 인스턴스 생성
config = configparser.ConfigParser()
config.read('config.ini')

# SQL 쿼리 및 기타 설정에 대한 구성

# 'batch' 테이블에서 최신 시작 번호를 가져오기 위한 SQL 쿼리
LATEST_START_NUM_QUERY = f"SELECT start_num FROM {config['Database']['batch_table_name']} ORDER BY start_num DESC LIMIT 1"

# 'sensor' 테이블에서 특정 번호부터 데이터를 가져오기 위한 SQL 템플릿
SENSOR_DATA_QUERY_TEMPLATE = f"SELECT * FROM {config['Database']['sensor_table_name']} WHERE number >= {{}}"
