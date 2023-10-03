from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import jwt_manager
import secrets

from db import db

import models

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
#Used to get User Blue Print
from resources.user import blp as UserBlueprint


def create_app(db_url=None):
    app = Flask(__name__)
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    #connects Flask App to sqlAlchemy
    db.init_app(app)
    api = Api(app)

    app.config["JWT_SECRET_KEY"] = "227779219714998987437280705912860315914"
    jwt = jwt_manager(app)
    
    with app.app_context():
        db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    #Registers User BluePrint In Flask Smorest - Shows API Documentation
    api.register_blueprint(UserBlueprint)

    return app

