from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims, jwt_optional, get_jwt_identity
from api.models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='Campo obrigatório.')

    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help='Store é obrigatório.')

    @jwt_required
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'item não foi encontrado.'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': 'Um item {} já esta cadastrado.'.format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {'message': 'Ocorreu um erro ao inserir o item.'}, 500

        return item.json(), 201

    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Você nao possui acesso.'}, 401

        item = ItemModel.find_by_name(name)
        if item:
            item.delete()

        return {'message': 'Item deletado'}, 400

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):

    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()

        itens = [item.json for item in ItemModel.list_itens()]
        if user_id:
            return {'itens': itens},
        return {
                   'item': [item['name'] for item in itens],
                   'message': 'Há mais dados se você logar.'
               }, 200
