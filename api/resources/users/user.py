from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp as equals
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
)
from api.models.user import User
from api.blacklist import BLACKLIST

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


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_jwt_identity()['jti']
        BLACKLIST.add(jti)
        return {'message': 'Usuário logout.'}, 200
