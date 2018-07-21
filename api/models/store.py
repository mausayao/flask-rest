from condb import db


class StoreModel(db.Model):
    __tablename__ = 'store'
    id = db.column(db.Integer, primary_key=True)
    name = db.column(db.String(80))

    itens = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name, price):
        self.name = name

    def json(self):
        return {'name': self.name, 'itens': [item.json() for item in self.itens.all()]}

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
        return {'itens': list(map(lambda x: x.json(), Store.query.all()))}
