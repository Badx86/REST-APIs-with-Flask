import os
import secrets
from db import db
from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint


def create_app(db_url=None):
    app = Flask(__name__)

    """
    Конфигурация приложения. PROPAGATE_EXCEPTIONS позволяет исключениям подниматься 
    и распространяться по стеку вызовов. API_TITLE, API_VERSION и OPENAPI_VERSION устанавливают
    базовую информацию для нашего API. OPENAPI_URL_PREFIX, OPENAPI_SWAGGER_UI_PATH и 
    OPENAPI_SWAGGER_UI_URL используются для настройки страницы Swagger UI
    """

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv(
        "DATABASE_URL", "sqlite:///data.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    api = Api(app)
    # 2 get your secret key: terminal -> python -> import secrets -> secrets.SystemRandom().getrandbits(128)
    app.config["JWT_SECRET_KEY"] = "test"
    jwt = JWTManager(app)

    @app.before_request
    def create_tables():
        db.create_all()

    """
    Регистрация blueprint в нашем API. Blueprint помогает делать 
    наше приложение модульным, организовывая функции нашего приложения
    в набор модулей. Здесь у нас есть два blueprint'а для Item и Store
    """

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app
