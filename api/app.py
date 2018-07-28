from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager as JWT
from api.resources.users.user import UserRegister, UserRes, UserLogin
from api.resources.itens.item import Item, ItemList
from api.resources.store.storeResource import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.bd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONs'] = True
app.config['JWT_SECRET_KEY'] = 'segredo'
# app.secret_key = 'segredo'
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

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/itens')

api.add_resource(UserRegister, '/register')
api.add_resource(UserRes, '/user/<int:user_id>')

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(UserLogin, '/login')

if __name__ == '__main__':
    from condb import db

    db.init_app(app)
    app.run(port=5000, debug=True)
