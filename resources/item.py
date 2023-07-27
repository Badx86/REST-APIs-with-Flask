import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models import ItemModel
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
        item = ItemModel.query.get_or_404(item_id)
        return item

    def delete(self, item_id):
        """Метод для удаления элемента по его ID"""
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted"}

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        """Метод для обновления элемента по его ID"""
        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()

        return item


@blp.route("/item")
class ItemList(MethodView):
    """Класс для работы со списком элементов"""

    @blp.response(200, ItemSchema(many=True))
    def get(self):
        """Метод для получения списка всех элементов"""
        return ItemModel.query.all()

    @blp.arguments(ItemSchema)
    @blp.response(200, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item")

        return item
