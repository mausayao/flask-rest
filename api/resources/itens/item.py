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
        item = Item.find_by_name(name)
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
        if Item.find_by_name(name):
            return {'message': 'Um item {} já esta cadastrado.'.format(name)}, 400

        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}

        connection =  sqlite3.connect('../../data.db')
        cursor = connection.cursor()

        query = 'INSERT INTO itens VLEUS (?, ?)'
        cursor.execute(query, (item.get('name'), item.get('price')))

        connection.commit()
        connection.close()

        return item, 201

    @jwt_required()
    def delete(self, name):
        global itens
        itens = list(filter(lambda x: x['name'] != name, itens))
        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, itens), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            itens.append(item)
        else:
            item.update(data)

        return item


class ItemList(Resource):

    def get(self):
        return {'item': itens}
