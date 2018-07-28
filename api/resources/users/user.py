from flask_restful import Resource, reqparse
from api.models.user import User


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='Campo nao pode ser vazio.')

    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='Campo nao pode ser vazio.')

    def post(self):
        data = UserRegister.parser.parse_args()

        user = User.find_by_username(data['username'])
        if user:
            return {'message': 'Usuário já cadastrado.'}, 400

        user = User(**data)
        user.save_to_db()

        return {'message': 'Usuário craido com sucesso.'}, 201


class UserRes(Resource):
    @classmethod
    def get(cls, user_id):
        user = User.find_by_id(user_id)
        if not user:
            return {'message': 'Usuário não foi encontrado.'},404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = User.find_by_id(user_id)
        if not user:
            return {'message': 'Usuário não foi encontrado.'}, 404
        user.delete_from_db()
        return {'message': 'Usuário foi deletado.'}