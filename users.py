

import models

from flask import Blueprint, request, session, render_template, redirect, url_for, flash

from passlib.hash import pbkdf2_sha256

users_bp = Blueprint('users', __name__)


@users_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return redirect(url_for('main.index'))


# 로그인
@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':

        id = request.form['id']
        password = request.form['pw']

        user = models.get_user(id)

        if user is None:
            flash('아이디 또는 비밀번호가 일치하지 않습니다.')
            return redirect(url_for('users.login'))

        if pbkdf2_sha256.verify(password, user['password']):
            session['user'] = user['id']
            return redirect(url_for('main.index'))
        else:
            flash('아이디 또는 비밀번호가 일치하지 않습니다.')
            return redirect(url_for('users.login'))


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

        enc_pw = pbkdf2_sha256.hash(password)

        result = models.register(id, name, email, enc_pw)

        if not result:
            error = '이미 존재하는 아이디입니다.'
            return render_template('register.html', error=error)

        return redirect(url_for('users.login'))


# 아이디 찾기
@users_bp.route('/findID', methods=['GET', 'POST'])
def find_id():
    if request.method == 'GET':
        return render_template('findID.html')

    elif request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        result = models.find_id(name, email)['id']
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

        result = models.find_user(id, name, email)

        if result:
            return render_template('findPW.html', result=result)
        else:
            return render_template('findPW.html', error=True)


# 내 프로필 보기
@users_bp.route('/my-profile', methods=['GET'])
def my_profile():
    if request.method == 'GET':
        user = session.get('user')
        if user is None:
            flash("로그인 후 이용할 수 있습니다.")
            return redirect(url_for('users.login'))

        my_boards = models.get_board(user)
        user = models.get_user(user)
        print(my_boards)
        print(user)

        return render_template('my-profile.html', user=user, boards=my_boards)


# @users_bp.route('/change-passwd', methods=['GET','POST'])
# def change_password(id):
#     if request.method == 'GET':
#         user = session.get('user')
#
#         if user is None &&:







    # user = models.get_user(user_id)
