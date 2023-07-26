# Определение схем с помощью Marshmallow
from marshmallow import Schema, fields

"""Marshmallow: библиотека в Python, предназначенная для преобразования сложных типов данных, таких как объекты, \
в Python примитивы и наоборот. Она используется для валидации, десериализации входящих данных \
и сериализации выходящих данных."""

"""Schema: в контексте Marshmallow, схема это класс, который определяет, как данные должны быть сериализованы \
или десериализованы. Каждое поле в схеме относится к полю в данных, которые вы хотите сериализовать/десериализовать, \
и определяет, как это должно быть сделано. Например, вы можете определить, что поле должно быть типа str, \
а если оно не является строкой, то произойдет ошибка"""


class ItemSchema(Schema):
    """Схема для создания элемента"""
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    store_id = fields.Str(required=True)


class ItemUpdateSchema(Schema):
    """Схема для обновления элемента"""
    name = fields.Str()
    price = fields.Float()


class StoreSchema(Schema):
    """Схема для магазина"""
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
