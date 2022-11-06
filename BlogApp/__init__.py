from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_migrate import Migrate



db = SQLAlchemy()
migrate = Migrate()
DB_NAME = "myblog.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'd571a82d75801c33edc9f536'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app) 
    migrate.init_app(app, db)
    

   

    from .blog import blog
    from .auth import auth

    app.register_blueprint(blog, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .datamodel import User, Post, Message

    with app.app_context():
        db.create_all()

    create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    return app

def create_database(app):
    if not path.exists("BlogApp/" + DB_NAME):
        print("Created database!")

    