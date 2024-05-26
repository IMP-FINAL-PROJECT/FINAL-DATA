import configparser

# 설정 파일을 읽기 위한 ConfigParser 인스턴스 생성
config = configparser.ConfigParser()
config.read('config.ini')

# 데이터베이스 테이블 이름 및 SQL 쿼리 템플릿 불러오기
BATCH_TABLE_NAME = config['Database']['batch_table_name']
SENSOR_TABLE_NAME = config['Database']['sensor_table_name']
DAILY_LIFE_PATTERN_TABLE_NAME = config['Database']['daily_life_pattern_table_name']

# SQL 쿼리 구성
# 'batch' 테이블에서 최신 시작 번호를 가져오기 위한 SQL 쿼리
LATEST_START_NUM_QUERY = f"SELECT start_num FROM {config['Database']['batch_table_name']} ORDER BY start_num DESC LIMIT 1"

# 'sensor' 테이블에서 특정 번호부터 데이터를 가져오기 위한 SQL 템플릿
SENSOR_DATA_QUERY_TEMPLATE = f"SELECT * FROM {config['Database']['sensor_table_name']} WHERE number >= {{}}"
DELETE_DAILY_LIFE_PATTERN_QUERY = """
    DELETE FROM daily_life_pattern WHERE id = %s AND date = %s;
    """
# 스크립트나 모듈에서 이 쿼리를 불러와 사용할 수 있습니다.
SENSOR_NUMBER_INDEX = int(config['Sensor']['SENSOR_NUMBER_INDEX'])
SENSOR_ID_INDEX = int(config['Sensor']['SENSOR_ID_INDEX'])
SENSOR_ILLUMINANCE_INDEX = int(config['Sensor']['SENSOR_ILLUMINANCE_INDEX'])
SENSOR_PEDOMETER_INDEX = int(config['Sensor']['SENSOR_PEDOMETER_INDEX'])
SENSOR_SCREEN_FREQUENCY_INDEX = int(config['Sensor']['SENSOR_SCREEN_FREQUENCY_INDEX'])
SENSOR_SCREEN_DURATION_INDEX = int(config['Sensor']['SENSOR_SCREEN_DURATION_INDEX'])
SENSOR_PHONE_FREQUENCY_INDEX = int(config['Sensor']['SENSOR_PHONE_FREQUENCY_INDEX'])
SENSOR_PHONE_DURATION_INDEX = int(config['Sensor']['SENSOR_PHONE_DURATION_INDEX'])
SENSOR_GPS_INDEX = int(config['Sensor']['SENSOR_GPS_INDEX'])
SENSOR_TIMESTAMP_INDEX = int(config['Sensor']['SENSOR_TIMESTAMP_INDEX'])
SENSOR_HOUR_INDEX = int(config['Sensor']['SENSOR_HOUR_INDEX'])