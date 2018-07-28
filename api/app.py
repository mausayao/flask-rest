from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager as JWT
from api.resources.users.user import UserRegister, UserRes, UserLogin, TokenRefresh, UserLogout
from api.resources.itens.item import Item, ItemList
from api.resources.store.storeResource import Store, StoreList
from api.blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.bd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONs'] = True
app.config['JWT_SECRET_KEY'] = 'segredo'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app)


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'Token expirou',
        'error': 'token_expired'
    }), 401


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': 'Assinatura inválida',
        'error': 'invalid_token'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description': 'Token expirado',
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoke_token_callback():
    return jsonify({
        'description': 'Token foi removido',
        'error': 'token_revoked'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback():
    return jsonify({
        'description': 'A requisição nao possui um token de acesso',
        'error': 'authorization_required'
    }), 401


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/itens')

api.add_resource(UserRegister, '/register')
api.add_resource(UserRes, '/user/<int:user_id>')

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')

if __name__ == '__main__':
    from condb import db

    db.init_app(app)
    app.run(port=5000, debug=True)
