import sqlite3
from flask_restful import Resource, reqparse


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
        connection = sqlite3.connect('../../data.db')
        cursor = connection.cursor()

        query = 'INSERT INTO users VALUES (NULL ,?, ?)'
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {'message': 'Usuário craido com sucesso'}, 201
