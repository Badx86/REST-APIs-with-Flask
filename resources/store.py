import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
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
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found.")

    def delete(self, store_id):
        """Метод для удаления магазина по его ID"""
        try:
            del stores[store_id]
            return {"message": "Store deleted."}
        except KeyError:
            abort(404, message="Store not found.")


# Создаем endpoint для получения списка магазинов и добавления нового магазина
@blp.route("/store")
class StoreList(MethodView):
    """Класс для работы со списком магазинов"""
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        """Метод для получения списка всех магазинов"""
        return stores.values()

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):
        """Метод для создания нового магазина"""
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message=f"Store already exists.")

        store_id = uuid.uuid4().hex
        store = {**store_data, "id": store_id}
        stores[store_id] = store
        return store
