

import models

from flask import Blueprint, request, session, render_template, redirect, url_for, flash

users_bp = Blueprint('users', __name__)


@users_bp.route('/logout', methods=['GET'])
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


# 로그인
@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':

        id = request.form['id']
        password = request.form['pw']

        user = models.get_user(id, password)

        if user is None:
            flash('존재하지 않는 계정입니다.')
            return redirect(url_for('login'))

        session['user'] = user

        return redirect(url_for('index'))


# 회원가입
@users_bp.route('/register', methods=['GET', 'POST'])
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
@users_bp.route('/findID', methods=['GET', 'POST'])
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
@users_bp.route('/findPW', methods=['GET', 'POST'])
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
@users_bp.route('/my-profile', methods=['GET'])
def my_profile():
    if request.method == 'GET':
        user = session.get('user')

        my_boards = models.get_board(user['id'])

        return render_template('my-profile.html', user=user, boards=my_boards)
