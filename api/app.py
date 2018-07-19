from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from api.security import authenticate, identity
from api.resources.users.user import UserRegister
from api.resources.itens.item import Item, ItemList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.bd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'segredo'
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/itens')

api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    from condb import db
    db.init_app(app)
    app.run(port=5000, debug=True)
