import secrets
import models
import posts

from flask import Flask, render_template, request, session, redirect, url_for, flash

app = Flask(__name__)

app.secret_key = secrets.token_hex(32)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        boards = models.get_all_boards()

        status = session.get('user')

        return render_template('index.html', boards=boards, status=status)

    elif request.method == 'POST':
        keyword = request.form['keyword']
        boards = models.get_board(keyword)
        return render_template('index.html', boards=boards)


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


# 로그인
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':

        id = request.form['id']
        password = request.form['pw']

        user = models.get_user(id, password)

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

        result = models.register(id, name, email, password)

        if not result:
            error = '이미 존재하는 아이디입니다.'
            return render_template('register.html', error=error)

        return redirect(url_for('login'))


# 아이디 찾기
@app.route('/findID', methods=['GET', 'POST'])
def find_id():
    if request.method == 'GET':
        return render_template('findID.html')

    elif request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        result = models.find_id(name, email)
        if not result:
            error = "존재하지 않는 사용자입니다."
            return render_template('findID.html', error=error)

        return render_template('findID.html', id=result)


# 비밀번호 찾기
@app.route('/findPW', methods=['GET', 'POST'])
def find_pw():
    if request.method == 'GET':
        return render_template('findPW.html')

    elif request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        email = request.form['email']

        result = models.find_passwd(id, name, email)

        if result:
            return render_template('findPW.html', result=result)
        else:
            return render_template('findPW.html', error=True)


# 내 프로필 보기
@app.route('/myprofile', methods=['GET', 'POST'])
def myprofile():
    if request.method == 'GET':
        return render_template('myprofile.html')


# 게시물 작성
@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'GET':
        return render_template('write.html')

    elif request.method == 'POST':

        if session.get('user') is None:
            flash("로그인 후 이용해주세요.")
            return redirect(url_for('login'))

        posts.write()



# 게시물 방문
@app.route('/post/<int:no>', methods=['GET', 'POST'])
def post(no):
    if request.method == 'GET':
        board = models.get_board(no)[0]

        # 요청을 보낸 클라이언트의 세션을 획득
        client = session.get('user')

        print(board['secret'])
        # 클라이언트의 id가 작성자의 id와 같은지 확인
        if client and client['id'] == board['id']:
            models.update_views(no)
            return render_template('post.html', board=board, author=True)
        elif board['secret'] == 1:    # 비밀 글의 경우 작성자가 아니면 확인불가
            flash("해당 글은 비밀글로 작성자만 볼 수 있습니다.")
            return redirect(url_for('index'))
        else:
            models.update_views(no)
            return render_template("post.html", board=board, author=False)

    elif request.method == 'POST':

        edit = request.form.get('edit')

        if edit == "수정":
            return redirect(url_for('update', no=no))
        elif edit == "삭제":
            models.delete_board(no)
            return redirect(url_for('index'))


# 게시글 수정
@app.route('/update/<int:no>', methods=['GET', 'POST'])
def update(no):
    if request.method == 'GET':
        board = models.get_board(no)[0]
        return render_template('update.html', board=board)

    elif request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        secret = request.form.get('secret', '0')

        if not title:
            flash("제목을 입력해주세요.")
            return redirect(url_for('update', no=no))
        elif not content:
            flash("내용을 입력해주세요.")
            return redirect(url_for('update', no=no))

        models.update_board(no, title, content, int(secret))
        print(secret)
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=5000)
