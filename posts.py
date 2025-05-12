import secrets
import models

from flask import Flask, render_template, request, session, redirect, url_for, flash

app = Flask(__name__)

app.secret_key = secrets.token_hex(32)

# 게시물 관련 기능

def write():
    title = request.form['title']
    content = request.form['content']
    secret = request.form.get('secret','0')

    if not title or not content:
        flash("빈칸을 모두 채워주세요.")
        return redirect(url_for('write'))

    else :
        models.create_Board(title, content, session['user']['id'], int(secret))



def view_post_noAuthor(No):
    edit = request.form.get('edit')

    if (edit == "수정"):
        return redirect(url_for('update', No=No))
    elif (edit == "삭제"):
        models.delete_board(No)