import DB_Connection.mysqlconnect as mysqlconnect
from .config import DELETE_DAILY_LIFE_PATTERN_QUERY


def delete_existing_entries(existing_entries_list):
    """
    existing_entries_list에 포함된 (id, date) 조합에 해당하는 레코드를 데이터베이스에서 삭제합니다.
    Parameters:
        existing_entries_list (list of tuple): 삭제할 레코드의 목록, 각 튜플은 (id, date) 형태입니다.
    """
    # DELETE 쿼리 실행
    mysqlconnect.excutemany_delete_query(DELETE_DAILY_LIFE_PATTERN_QUERY, existing_entries_list)
