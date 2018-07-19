import sqlite3
from condb import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.column(db.Integer, primary_key=True)
    username = db.column(db.String(80))
    password = db.column(db.String(89))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, name):
        return cls.query.filter_by(username=name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
