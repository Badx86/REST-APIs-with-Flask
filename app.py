import os
import secrets
from db import db
from flask_smorest import Api
from blocklist import BLOCKLIST
from flask import Flask, jsonify
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

    app.config["JWT_SECRET_KEY"] = "test"  # ключ для подписи JWT
    jwt = JWTManager(app)  # создание экземпляра менеджера JWT

    """
    В данном контексте JWT (JSON Web Tokens) используется для реализации аутентификации и авторизации пользователей \
    в приложении. JWT - это стандарт, который определяет способ безопасной передачи информации между двумя сторонами \
    в виде JSON-объекта. Эта информация может быть верифицирована и доверена, поскольку она подписана.

    Использование JWT в этом коде включает в себя определение дополнительных претензий (claims), которые используются \
    для передачи данных о пользователе внутри токена. В этом случае есть претензия "is_admin", которая определяет, \
    является ли пользователь администратором или нет.
    
    JWT также обрабатывает различные ошибки, связанные с токеном, такие как истекший токен, недействительный токен \
    или отсутствующий токен. Он возвращает соответствующие сообщения об ошибках и коды статуса HTTP
    """

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked", "error": "token_revoked"}
            ),
            401,
        )

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        """Добавление дополнительных претензий (claims) к JWT"""
        if identity == 1:  # Если идентификатор пользователя равен 1, считаем его администратором
            return {"is_admin": True}
        return {"is_admin": False}  # В противном случае пользователь не является администратором

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        """Обратный вызов для случая, когда токен истек"""
        return (
            jsonify({"message": "The token has expired", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token",
                    "error": "authorization_required",
                }
            ),
            401,
        )

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
