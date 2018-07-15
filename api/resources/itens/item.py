from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from api.models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='Campo obrigatório.')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'item não foi encontrado.'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': 'Um item {} já esta cadastrado.'.format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'])

        try:
            item.insert_item()
        except:
            return {'message': 'Ocorreu um erro ao inserir o item.'}, 500

        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        try:
            ItemModel.delete_item(name)
            return {'message': 'Item foi excluido.'}
        except:
            return {'message': 'Erro ao excluir item.'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, data['price'])
            try:
                item.insert_item()
            except:
                return {'message': 'Ocorreu um erro ao inserir o item.'}, 500

        else:
            try:
                item.update_item()
            except:
                return {'message': 'Ocorreu um erro ao editar o item.'}, 500

        return item.json()


class ItemList(Resource):

    def get(self):
        itens = ItemModel.list_itens()
        return {'item': itens}
