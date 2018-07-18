import sqlite3
from condb import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.column(db.Integer, primary_key=True)
    username = db.column(db.String(80))
    password = db.column(db.String(89))

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, name):
        connection = sqlite3.connect('../data.db')
        cursor = connection.cursor()

        select = 'SELECT * FROM users WHERE username=?'

        result = cursor.execute(select, (name,))
        row = result.fetchone()

        if row:
            user = cls(*row)
        else:
            user = None

        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('../data.db')
        cursor = connection.cursor()

        select = 'SELECT * FROM users WHERE id=?'

        result = cursor.execute(select, (_id,))
        row = result.fetchone()

        if row:
            user = cls(*row)
        else:
            user = None

        return user
