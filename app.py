import secrets
import models

from flask import Flask, render_template, request, session, redirect, url_for, flash

app = Flask(__name__)

app.secret_key = secrets.token_hex(32)


@app.route('/')
def index():
    boards = models.get_allBoards()
    return render_template('index.html', boards=boards)


# 로그인
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

        # 로그인시 세션 생성
        session['user'] = user

        return redirect(url_for('index'))


# 회원가입
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


# 게시물 작성
@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'GET':
        return render_template('write.html')

    elif request.method == 'POST':

        title = request.form['title']
        content = request.form['content']

        if session.get('user') is None:
            flash("로그인 후 이용해주세요.")
            return redirect(url_for('login'))

        if not title or not content:
            flash("빈칸을 채워주세요.")
            return redirect(url_for('write'))


        models.create_Board(title, content, session['user']['id'])

        return redirect(url_for('index'))


# 게시물 방문
@app.route('/post/<int:No>', methods=['GET','POST'])
def post(No):
    if request.method == 'GET':
        board = models.get_board(No)
        models.update_views(No)

        # 요청을 보낸 클라이언트의 세션을 획득
        is_author = session.get('user')

        # 클라이언트의 id가 작성자의 id와 같은지 확인
        if is_author and is_author['id'] == session['user']['id']:
            return render_template('post.html', board=board, author=True)
        else:
            return render_template("post.html", board=board)

    elif request.method == 'POST':

        edit = request.form.get('edit')

        if (edit == "수정"):
            return redirect(url_for('update', No=No))
        elif (edit == "삭제"):
            models.delete_Board(No)
            return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=5000)


@app.route('/update/<int:No>', methods=['GET', 'POST'])
def update(No):
    if request.method == 'GET':
        board = models.get_board(No)
        return render_template('update.html', board=board)

    elif request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            error = "제목을 입력해주세요."
            return render_template('update.html', error=error)
        elif not content:
            error = "내용을 입력해주세요."
            return render_template('update.html', error=error)

        models.update_Board(No, title, content)
        return redirect(url_for('index'))
