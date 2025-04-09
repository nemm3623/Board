import secrets
import models

from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)

app.secret_key = secrets.token_hex(32)


@app.route('/')
def index():
    boards = models.get_allBoards()
    print(boards)
    return render_template('index.html', boards=boards)


############ 로그인 ##############
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':

        id = request.form['id']
        password = request.form['pw']

        user = models.get_User(id, password)

        if user is None:
            error = '존재하지 않는 계정입니다.'
            return render_template('login.html', error=error)

        session['user'] = user

        return redirect(url_for('index'))

############### 회원가입 ###############
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    elif request.method == 'POST':

        id = request.form['id']
        email = request.form['email']
        name = request.form['name']
        password = request.form['pw']

        if not id or not email or not name or not password:
            error = "빈칸을 채워주세요."
            return render_template('register.html', error=error)

        result = models.get_User(id, password)

        if not result:
            error = '이미 존재하는 아이디입니다.'
            return render_template("register.html", error=error)

        return redirect(url_for('login'))


@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'GET':
        return render_template('write.html')

    elif request.method == 'POST':

        title = request.form['title']
        content = request.form['content']

        if not title:
            error = "제목을 입력해주세요."
            return render_template('write.html', error=error)
        elif not content:
            error = "내용을 입력해주세요."
            return render_template('write.html', error=error)

        board = {"title": title, "content": content, "id": session['user']["id"]}
        models.create_Board(board)

        print("clear2")

        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=5000)
