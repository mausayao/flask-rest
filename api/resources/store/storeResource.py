from flask_restful import Resource, reqparse
from api.models.store import StoreModel


class Store(Resource):

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        return {'message': 'Item não encontrado'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': 'A loja {} já existe'.format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db();
        except:
            return {'message': 'Ocorreu um erro ao tentar cria a loja {}'.format(name)}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete()

        return {'message': 'A loja foi deletada.'}


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.list_itens()]}
