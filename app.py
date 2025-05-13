import secrets

import models

from flask import Flask, render_template, request, session

from users import users_bp

from posts import posts_bp

app = Flask(__name__)

app.register_blueprint(users_bp)
app.register_blueprint(posts_bp)


app.secret_key = secrets.token_hex(32)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':

        boards = models.get_all_boards()
        status = session.get('user')
        user_list = models.get_all_user()

        return render_template('index.html', boards=boards, list=user_list, status=status)

    elif request.method == 'POST':
        keyword = request.form.get('keyword', '')
        boards = models.get_board(keyword)
        user_list = models.get_all_user()

        return render_template('index.html', boards=boards, list=user_list, status=session.get('user'))


if __name__ == '__main__':
    app.run(port=5000)
