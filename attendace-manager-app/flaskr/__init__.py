# __ init__.py
from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# ログインマネージャの設定
login_manager = LoginManager()
login_manager.login_view = 'app.login'
login_manager.login_message = 'ログインしていません. ログインして下さい.'

# SQLAlchemy, Migrateの初期化
db = SQLAlchemy()
migrate = Migrate()

# 実行メソッド
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'mysite'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/postgres'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    from flaskr.views import bp
    app.register_blueprint(bp)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    return app

