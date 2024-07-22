#music v2/backend/Mysite/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .instances import cache








db = SQLAlchemy()
db_name = "mydatabase.sqlite3"

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "Anish_key"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_name}"
    UPLOAD_FOLDER = 'static/upload'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['CACHE_TYPE'] = 'RedisCache'
    app.config['CACHE_REDIS_HOST'] = 'localhost'
    app.config['CACHE_REDIS_PORT'] = 6379
    app.config['CACHE_REDIS_DB'] = 3

   


   
    
    db.init_app(app)
    CORS(app, supports_credentials=True)
    cache.init_app(app)


    from .views import views
    from .auth import auth
    from .song import songs
    from .playlist import playlist
    from .album import album



    from .model import User,Song,Rating,Playlist,Album
     
    # with app.app_context():
    #    create_database()

    JWTManager(app)

   
        
    app.register_blueprint(songs)
    app.register_blueprint(playlist)
    app.register_blueprint(album)
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    



    return app


def create_database():
    if not path.exists(db_name):
        db.create_all()
        print("Created Database !")
