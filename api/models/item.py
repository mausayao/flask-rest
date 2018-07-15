import sqlite3


class ItemModel:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('../../data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM itens WHERE name = ?'

        cursor.execute(query, (name,))
        row = cursor.fetchone()
        connection.close()

        if row:
            return cls(*row)

    def update_item(self):
        connection = sqlite3.connect()
        cursor = connection.cursor()

        query = 'UPDATE itens SET price=? WHERE name=?'
        cursor.execute(query, (self.price, self.name))

        connection.commit()
        connection.close()

    def insert_item(self):
        connection = sqlite3.connect('../../data.db')
        cursor = connection.cursor()

        query = 'INSERT INTO itens VALUES (?, ?)'
        cursor.execute(query, (self.name, self.price))

        connection.commit()
        connection.close()

    @classmethod
    def delete_item(cls, name):
        connection = sqlite3.connect('../../data.db')
        cursor = connection.cursor()

        query = 'DELETE FROM itens WHERE name = ?'
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

    @classmethod
    def list_itens(cls):
        connection = sqlite3.connect('../../data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM itens'
        rows = cursor.execute(query).fetchall()

        itens = []
        for row in rows:
            item = {'name': row[0], 'price': row[1]}
            itens.append(item)

        return itens
