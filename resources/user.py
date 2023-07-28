import os
import redis
from rq import Queue
from tasks import send_user_registration_email
from flask import current_app
from flask.views import MethodView
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, create_refresh_token, get_jwt_identity
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from blocklist import BLOCKLIST
from sqlalchemy import or_
from db import db
from models import UserModel
from schemas import UserSchema, UserRegisterSchema

# Создаем Blueprint для работы с пользователями
blp = Blueprint("Users", "users", description="Operations on users")

connection = redis.from_url(
    os.getenv("REDIS_URL")
)  # Get this from Render.com or run in Docker
queue = Queue("emails", connection=connection)


@blp.route("/register")
class UserRegister(MethodView):
    """Класс для регистрации нового пользователя"""

    @blp.arguments(UserRegisterSchema)
    def post(self, user_data):
        """Метод регистрации нового пользователя"""
        if UserModel.query.filter(
                or_(
                    UserModel.username == user_data["username"],
                    UserModel.email == user_data["email"]
                )
        ).first():
            abort(409, message="A user with that username already exists")

        user = UserModel(
            username=user_data["username"],
            email=user_data["email"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )
        db.session.add(user)
        db.session.commit()

        current_app.queue.enqueue(send_user_registration_email, user.email, user.username)

        return {"message": "User created successfully"}, 201

@blp.route("/login")
class UserLogin(MethodView):
    """Класс для входа пользователя в систему"""

    @blp.arguments(UserSchema)
    def post(self, user_data):
        """Метод для аутентификации пользователя и получения токена"""
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        abort(401, message="Invalid credentials")


@blp.route("/refresh")
class TokenRefresh(MethodView):
    """Класс для обновления токена пользователя"""

    @jwt_required(refresh=True)
    def post(self):
        """Метод для обновления токена доступа"""
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"access_token": new_token}, 200


@blp.route("/logout")
class UserLogout(MethodView):
    """Класс для выхода пользователя из системы"""

    @jwt_required()
    def post(self):
        """Метод для выхода пользователя из системы и добавления токена в блок-лист"""
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200


@blp.route("/user/<int:user_id>")
class User(MethodView):
    """
    Этот ресурс может быть полезен при тестировании нашего Flask-приложения. \
    Возможно, мы не захотим предоставлять к нему доступ общественности, но для демонстрации \
    в рамках этого курса он может быть полезен, когда мы работаем с данными пользователей.
    """

    @blp.response(200, UserSchema)
    def get(self, user_id):
        """Метод для получения информации о пользователе по его ID"""
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        """Метод для удаления пользователя по его ID"""
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}, 200
