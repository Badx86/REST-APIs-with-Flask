import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from models import StoreModel
from schemas import StoreSchema

# Создаем новый Blueprint
blp = Blueprint("stores", __name__, description="Operations on stores")


# Создаем endpoint для работы с конкретным магазином
@blp.route("/store/<string:store_id>")
class Store(MethodView):
    """Класс для работы с отдельным магазином"""
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        """Метод для получения информации о магазине по его ID"""
        store = StoreModel.query.get_or_404(self, store_id)
        return store

    def delete(self, store_id):
        """Метод для удаления магазина по его ID"""
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted"}, 200


# Создаем endpoint для получения списка магазинов и добавления нового магазина
@blp.route("/store")
class StoreList(MethodView):
    """Класс для работы со списком магазинов"""
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        """Метод для получения списка всех магазинов"""
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A store with that name already exists",)
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item")

        return store
