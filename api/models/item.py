from condb import db


class ItemModel(db.Model):
    __tablename__ = 'itens'
    id = db.column(db.Integer, primary_key=True)
    name = db.column(db.String(80))
    price = db.column(db.Float(precision=2))

    store_id = db.column(db.Integer, db.ForeignKey('store.id'))

    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_item(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def list_itens(cls):
        return {'itens': list(map(lambda x: x.json(), ItemModel.query.all()))}
