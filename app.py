import secrets

from flask import Flask

from users import users_bp
from posts import posts_bp
from main import main_bp

app = Flask(__name__)

app.register_blueprint(users_bp)
app.register_blueprint(posts_bp)
app.register_blueprint(main_bp)

app.secret_key = secrets.token_hex(32)


if __name__ == '__main__':
    app.run(port=5000)
