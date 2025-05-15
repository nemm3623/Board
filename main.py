import models

from flask import Blueprint, render_template, request, session


main_bp = Blueprint('main', __name__)


@main_bp.route('/', methods=['GET', 'POST'])
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
