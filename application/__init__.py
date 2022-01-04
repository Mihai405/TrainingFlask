from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_caching import Cache
import os

db = SQLAlchemy()
bcrypt = Bcrypt()
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})

def create_app(test_config=None):
    basedir = os.path.abspath(os.path.dirname(__file__))
    app = Flask(__name__)
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    if test_config is not None:
        app.config.update(test_config)
    db.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)

    #local imports
    from .friends import friends
    from .users import users
    app.register_blueprint(friends, url_prefix="/friends/")
    app.register_blueprint(users, url_prefix="/users/")

    return app