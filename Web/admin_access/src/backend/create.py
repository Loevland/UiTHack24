import sqlite3

conn = sqlite3.connect('database.sqlite')
c = conn.cursor()
c.execute('''CREATE TABLE users (username TEXT, password TEXT, flag TEXT)''')
c.execute("INSERT INTO users (username, password, flag) VALUES ('admin', 'asdfmjpagy0123jgla09+213kasgf032', 'UiTHack24{SqL_1nj3ct10n_1s_4m4z1ng}')")
conn.commit()
conn.close()
