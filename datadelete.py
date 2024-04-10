import mysqlconnect

def delete_existing_entries(existing_entries_list):
    """
    existing_entries_list에 포함된 (id, date) 조합에 해당하는 레코드를 데이터베이스에서 삭제하는 함수
    """
    # DELETE 쿼리 템플릿
    delete_query = """
    DELETE FROM daily_life_pattern WHERE id = %s AND date = %s;
    """
    # DELETE 수행 함수 호출

    mysqlconnect.excutemany_delete_query(delete_query,existing_entries_list)
