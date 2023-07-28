from db import db


class StoreModel(db.Model):
    """
    Модель представляет таблицу 'stores' в базе данных
    Связывает объект StoreModel с таблицей 'stores' в базе данных и определяет его структуру
    """

    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    items = db.relationship(
        "ItemModel", back_populates="store", lazy="dynamic", cascade="all, delete"
    )
    tags = db.relationship("TagModel", back_populates="store", lazy="dynamic")
