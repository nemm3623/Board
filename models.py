import pymysql
from pymysql import cursors


def get_connection():

    db_connection = pymysql.connect(
        host='localhost',
        user='root',
        passwd='',
        database='Board',
        charset='utf8mb4',
        cursorclass=cursors.DictCursor
    )

    return db_connection, db_connection.cursor()

# 모든 게시물
def get_allBoards() :

    db_connection, cursor = get_connection()

    query = "SELECT * FROM Boards"
    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    db_connection.close()

    return result

# 게시물 찾기
def get_Board(No):
    db_connection, cursor = get_connection()

    # 튜플이 아닌 문자열이나 정수로 값을 넘기면 excute()는 시퀀스를 요구하기 때문에 에러발생
    # EX) "abcd" -> 'a', 'b', 'c', 'd' 로 해석
    query = "SELECT * FROM Boards WHERE No=%s"
    cursor.execute(query, (No,))
    result = cursor.fetchone()

    cursor.close()
    db_connection.close()

    return result

def create_Board(title, content, id):
    db_connection, cursor = get_connection()

    query = "INSERT INTO Boards (title, content, id) VALUES (%s, %s, %s)"
    cursor.execute(query, (title,content,id))

    db_connection.commit()

    cursor.close()
    db_connection.close()

# 유저 찾기
def get_User(id, pw):
    db_connection, cursor = get_connection()

    query = "SELECT * FROM Users WHERE id = %s and password = %s"
    cursor.execute(query, (id,pw))
    result = cursor.fetchone()

    cursor.close()
    db_connection.close()

    return result

# 회원가입
def register(id, name, email, password):
    db_connection, cursor = get_connection()

    query = "SELECT * FROM Users WHERE id = %s"
    cursor.execute(query, (id,))
    result = cursor.fetchone()

    if result :
        cursor.close()
        db_connection.close()
        return False

    query = "INSERT INTO Users (id, name, email, password) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (id, name, email, password))

    # DB의 변경사항을 진짜 저장, INSERT 혹은 UPDATE는 execute()를 한 것으로는 진짜 저장이 되지 않음
    db_connection.commit()

    cursor.close()
    db_connection.close()

    return True



