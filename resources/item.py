import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ItemSchema, ItemUpdateSchema

"""Blueprint: способ организации группы связанных между собой маршрутов, функций представления и других кодовых \
элементов, которые можно использовать несколько раз. Он позволяет разделять приложение на логические блоки, \
которые можно использовать в разных частях приложения"""

# Создаем новый Blueprint для работы с элементами (items)
blp = Blueprint("Items", __name__, description="Operations on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    """Класс для работы с отдельным элементом"""
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        """Метод для получения информации об элементе по его ID"""
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found.")

    def delete(self, item_id):
        """Метод для удаления элемента по его ID"""
        try:
            del items[item_id]
            return {"message": "Item deleted."}
        except KeyError:
            abort(404, message="Item not found.")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        """Метод для обновления элемента по его ID"""
        try:
            item = items[item_id]
            # Объединяем текущие данные элемента с обновленными данными
            item |= item_data

            return item
        except KeyError:
            abort(404, message="Item not found.")


@blp.route("/item")
class ItemList(MethodView):
    """Класс для работы со списком элементов"""
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        """Метод для получения списка всех элементов"""
        return items.values()

    @blp.arguments(ItemSchema)
    @blp.response(200, ItemSchema)
    def post(self, item_data):
        """Метод для создания нового элемента"""
        for item in items.values():
            if (
                    item_data["name"] == item["name"]
                    and item_data["store_id"] == item["store_id"]
            ):
                abort(400, message=f"Item already exists.")

        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item

        return item
