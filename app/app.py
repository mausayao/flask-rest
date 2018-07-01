from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from app.security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'segredo'
api = Api(app)

jwt = JWT(app, authenticate, identity)

itens = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='Campo obrigatório.')

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, itens), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, itens), None):
            return {'message': 'Um item {} já esta cadastrado.'.format(name)}, 400

        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        itens.append(itens)
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


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/itens')

app.run(port=5000, debug=True)
