import pymysql
from flask import Flask, render_template, request, flash, redirect, url_for
from pymysql import cursors

app = Flask(__name__)

db_connection = pymysql.connect(
    host='localhost',
    user='root',
    passwd='',
    database='Board',
    charset='utf8mb4',
    cursorclass=cursors.DictCursor
)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        id = request.form['id']
        password = request.form['pw']
        cursor = db_connection.cursor()

        cursor.execute(f'SELECT * FROM users WHERE id={id} and password={password}')
        user = cursor.fetchone()

        if user is None:
            flash('ID 혹은 Password가 올바르지 않습니다.')
            #return redirect(url_for('login'))

        return render_template('login.html')


if __name__ == '__main__':
    app.run(port=5000)
