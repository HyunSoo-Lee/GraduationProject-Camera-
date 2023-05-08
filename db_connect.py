import pymysql

# 연결 정보
host = 'graduation-database.cicoecqa7q2u.ap-northeast-2.rds.amazonaws.com'
user = 'admin'
password = 'sean9045'
database = 'graduationdb'

def find_row(table_name, column_name, user_name, host = host, user = user, password = password, database = database):
    # 데이터베이스 연결
    connection = pymysql.connect(host=host, user=user, password=password, database=database)

    # 커서 생성
    cursor = connection.cursor()

    # 쿼리 실행
    query = f"SELECT * FROM {table_name} WHERE {column_name} = '{user_name}'"
    cursor.execute(query)

    # 결과 가져오기
    result = cursor.fetchall()
    if result:
            for row in result:
                print(row)
    else:
        print("query error occured!")
    # 연결 종료
    cursor.close()
    connection.close()

def find_id(table_name, column_name, user_name, host = host, user = user, password = password, database = database):
    connection = pymysql.connect(host=host, user=user, password=password, database=database)

    # 커서 생성
    cursor = connection.cursor()

    # 쿼리 실행
    query = f"SELECT user_id FROM {table_name} WHERE {column_name} = '{user_name}'"
    cursor.execute(query)

    # 결과 가져오기
    result = cursor.fetchone()
    if result:
            value = result[0]
            print(value)

    else:
        print("query error occured!")
    # 연결 종료
    cursor.close()
    connection.close()
    return value

def edit_time(table_name, column_name, user_name, host = host, user = user, password = password, database = database):
    connection = pymysql.connect(host=host, user=user, password=password, database=database)
     # 커서 생성
    cursor = connection.cursor()

    # 쿼리 실행
    query = "UPDATE your_table SET your_datetime_column = %s WHERE <condition>"  # datetime 칼럼을 수정하는 쿼리
    cursor.execute(query, (new_value,))  # datetime 값은 튜플로 전달해야 하므로 (new_value,) 형태로 전달

    # 변경 사항 저장
    connection.commit()

    # 연결 종료
    cursor.close()
    connection.close()