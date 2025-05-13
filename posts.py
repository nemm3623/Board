import models

from flask import Blueprint, render_template, request, session, redirect, url_for, flash

posts_bp = Blueprint('posts', __name__)


# 게시물 작성
@posts_bp.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'GET':
        return render_template('write.html')

    elif request.method == 'POST':

        if session.get('user') is None:
            flash("로그인 후 이용해주세요.")
            return redirect(url_for('users.login'))

        title = request.form.get('title', '')
        content = request.form.get('content', '')
        secret = request.form.get('secret', '0')

        if not title or not content:
            flash("빈칸을 모두 채워주세요.")
            return redirect(url_for('write'))

        else:
            models.create_Board(title, content, session['user']['id'], int(secret))


# 게시물 방문
@posts_bp.route('/post/<int:no>', methods=['GET', 'POST'])
def post(no):
    if request.method == 'GET':
        board = models.get_board(no)[0]

        # 요청을 보낸 클라이언트의 세션을 획득
        client = session.get('user')

        # 클라이언트의 id가 작성자의 id와 같은지 확인
        is_author(board, client, no)

    elif request.method == 'POST':

        status = request.form.get('edit')

        if status == "수정":
            return redirect(url_for('update', no=no))
        elif status == "삭제":
            models.delete_board(no)
            return redirect(url_for('index'))


# 게시글 수정
@posts_bp.route('/update/<int:no>', methods=['GET', 'POST'])
def edit(no):
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

        return redirect(url_for('index'))


def is_author(board, client, no):

    if client and client['id'] == board['id']:
        models.update_views(no)
        return render_template('post.html', board=board, author=True)
    elif board['secret'] == 1:    # 비밀 글의 경우 작성자가 아니면 확인불가
        flash("해당 글은 비밀글로 작성자만 볼 수 있습니다.")
        return redirect(url_for('index'))
    else:
        models.update_views(no)
        return render_template("post.html", board=board, author=False)
