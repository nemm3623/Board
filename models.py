import pymysql
from pymysql import cursors


def get_connection():
    db_connection = pymysql.connect(
        host='localhost',
        user='root',
        passwd='wnsdud2ekr',
        database='Board',
        charset='utf8mb4',
        cursorclass=cursors.DictCursor
    )

    return db_connection, db_connection.cursor()


# 모든 게시물
def get_all_boards():
    db_connection, cursor = get_connection()

    query = "SELECT * FROM Boards"
    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    db_connection.close()

    return result


# 게시물 찾기
def get_board(keyword=None):
    db_connection, cursor = get_connection()

    if keyword is None:
        return get_all_boards()

    new_word = f"%{keyword}%"

    try:
        no = int(keyword)
        query = "SELECT * FROM Boards WHERE No = %s OR id = %s OR title LIKE %s"
        cursor.execute(query, (no, new_word, new_word))

    except ValueError:
        # keyword가 숫자가 아니면 No 비교는 제외
        query = "SELECT * FROM Boards WHERE id = %s OR title LIKE %s"
        cursor.execute(query, (new_word, new_word))

    result = cursor.fetchall()
    cursor.close()
    db_connection.close()

    return result


# 게시물 작성
def create_Board(title, content, id, secret):
    db_connection, cursor = get_connection()
    print(secret)
    query = "INSERT INTO Boards (title, content, id,secret) VALUES (%s, %s, %s,%s)"
    cursor.execute(query, (title, content, id, secret))

    db_connection.commit()

    cursor.close()
    db_connection.close()


# 게시물 조회수 업데이트
def update_views(No):
    db_connection, cursor = get_connection()

    query = "UPDATE Boards SET views = views + 1 WHERE No=%s"
    cursor.execute(query, (No,))

    db_connection.commit()
    cursor.close()
    db_connection.close()


# 게시물 수정
def update_board(no, title, content, secret):
    db_connection, cursor = get_connection()

    query = "UPDATE Boards SET title = %s, content = %s, secret = %s WHERE No=%s"
    cursor.execute(query, (title, content, int(secret), no))

    db_connection.commit()
    cursor.close()
    db_connection.close()


# 게시물 삭제
def delete_board(no):
    db_connection, cursor = get_connection()
    query = "DELETE FROM Boards WHERE No=%s"
    cursor.execute(query, (no))

    db_connection.commit()
    cursor.close()
    db_connection.close()


def get_all_user():
    db_connection, cursor = get_connection()

    query = "SELECT * FROM Users"
    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    db_connection.close()

    return result


# 로그인
def get_user(id):
    db_connection, cursor = get_connection()

    query = "SELECT * FROM Users WHERE id = %s"
    cursor.execute(query, (id, ))
    result = cursor.fetchone()

    cursor.close()
    db_connection.close()

    return result


# 회원가입
def register(id, name, email, password):
    db_connection, cursor = get_connection()

    query = "SELECT * FROM Users WHERE id = %s or email = %s"
    cursor.execute(query, (id, email))
    result = cursor.fetchone()

    if result:
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


# 아이디 찾기
def find_id(name, email):
    db_connection, cursor = get_connection()

    query = "SELECT id FROM Users WHERE name = %s AND email = %s"
    cursor.execute(query, (name, email))
    result = cursor.fetchone()

    cursor.close()
    db_connection.close()

    return result


# 비밀번호 찾기
def find_user(id, name, email):
    db_connection, cursor = get_connection()

    query = "SELECT * FROM Users WHERE id = %s AND name = %s AND email = %s"
    cursor.execute(query, (id, name, email))
    result = cursor.fetchone()

    cursor.close()
    db_connection.close()

    return result
