from db import db


class ItemModel(db.Model):
    """
    Модель представляет таблицу 'items' в базе данных
    Связывает объект ItemModel с таблицей 'items' в базе данных и определяет его структуру
    """
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False)
    store = db.relationship("StoreModel", back_populates="items")