import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table_user = 'CREATE TABLE IF NOT  EXISTS users(id INTEGER PRIMARY KEY , username text, password text)'

cursor.execute(create_table_user)

connection.commit()
connection.close()
