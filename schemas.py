# Определение схем с помощью Marshmallow
from marshmallow import Schema, fields

"""Marshmallow: библиотека в Python, предназначенная для преобразования сложных типов данных, таких как объекты, \
в Python примитивы и наоборот. Она используется для валидации, десериализации входящих данных \
и сериализации выходящих данных."""

"""Schema: в контексте Marshmallow, схема это класс, который определяет, как данные должны быть сериализованы \
или десериализованы. Каждое поле в схеме относится к полю в данных, которые вы хотите сериализовать/десериализовать, \
и определяет, как это должно быть сделано. Например, вы можете определить, что поле должно быть типа str, \
а если оно не является строкой, то произойдет ошибка"""


class PlainItemSchema(Schema):
    """Схема для создания элемента"""
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)


class PlainStoreSchema(Schema):
    """Схема для магазина"""
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class ItemUpdateSchema(Schema):
    """Схема для обновления элемента"""
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()


class ItemSchema(PlainItemSchema):
    """Схема для полного представления элемента, включая информацию о связанном магазине"""
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)


class StoreSchema(PlainStoreSchema):
    """Схема для полного представления магазина, включая информацию о связанных элементах"""
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
