from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp as equals
from flask_jwt_extended import create_access_token, create_refresh_token
from api.models.user import User

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                    type=str,
                    required=True,
                    help='Campo nao pode ser vazio.')

_user_parser.add_argument('password',
                    type=str,
                    required=True,
                    help='Campo nao pode ser vazio.')


class UserRegister(Resource):

    def post(self):
        data = _user_parser.parser.parse_args()

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
            return {'message': 'Usuário não foi encontrado.'}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = User.find_by_id(user_id)
        if not user:
            return {'message': 'Usuário não foi encontrado.'}, 404
        user.delete_from_db()
        return {'message': 'Usuário foi deletado.'}


class UserLogin(Resource):

    @classmethod
    def post(cls):
        data = _user_parser.parser.parse_args()

        user = User.find_by_username(data['username'])
        if user and equals(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)

            return {
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 200

        return {'message': 'Usuário ou senha inválido'}, 401
