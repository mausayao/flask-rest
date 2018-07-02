import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table_user = 'CREATE TABLE users(id int, username text, password text)'

cursor.execute(create_table_user)

user = (1, 'admin', 'admin')

insert_user = 'INSERT INTO users VALUES (?, ?, ?)'

cursor.execute(insert_user, user)

users = [
    (2, 'ezi', 'ezi'),
    (3, 'zuli', 'zuli'),
    (4, 'gil', 'gil')
]

cursor.executemany(insert_user, users)

connection.commit()
connection.close()
