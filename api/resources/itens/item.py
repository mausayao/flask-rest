from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='Campo obrigatório.')

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'item não foi encontrado.'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('../../data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM itens WHERE name = ?'

        cursor.execute(query, (name,))
        row = cursor.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    def post(self, name):
        if self.find_by_name(name):
            return {'message': 'Um item {} já esta cadastrado.'.format(name)}, 400

        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}

        try:
            self.insert_item(item)
        except:
            return {'message': 'Ocorreu um erro ao inserir o item.'}, 500

        return item, 201

    @jwt_required()
    def delete(self, name):

        connection = sqlite3.connect('../../data.db')
        cursor = connection.cursor()

        query = 'DELETE FROM itens WHERE name = ?'
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = Item.find_by_name(name)
        if item is None:
            item = {'name': name, 'price': data['price']}
            try:
                self.insert_item(item)
            except:
                return {'message': 'Ocorreu um erro ao inserir o item.'}, 500

        else:
            try:
                self.update_item(item)
            except:
                return {'message': 'Ocorreu um erro ao editar o item.'}, 500

        return item

    @classmethod
    def update_item(cls, item):
        connection = sqlite3.connect()
        cursor = connection.cursor()

        query = 'UPDATE itens SET price=? WHERE name=?'
        cursor.execute(query, (item.get('price'), item.get('name')))

        connection.commit()
        connection.close()

    @classmethod
    def insert_item(cls, item):
        connection = sqlite3.connect('../../data.db')
        cursor = connection.cursor()

        query = 'INSERT INTO itens VALUES (?, ?)'
        cursor.execute(query, (item.get('name'), item.get('price')))

        connection.commit()
        connection.close()


class ItemList(Resource):

    def get(self):
        itens = self.list_itens()
        return {'item': itens}

    @classmethod
    def list_itens(cls):
        connection = sqlite3.connect('../../data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM itens'
        rows = cursor.execute().fetchall()

        itens = []
        for row in rows:
            item = {'name': row[0], 'price': row[1]}
            itens.append(item)

        return itens
