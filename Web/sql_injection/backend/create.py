import sqlite3

conn = sqlite3.connect('database.sqlite')
c = conn.cursor()
c.execute('''CREATE TABLE users (username TEXT, password TEXT, flag TEXT)''')
c.execute("INSERT INTO users (username, password, flag) VALUES ('admin', 'asdfmjpagy0123jgla09+213kasgf032', 'Uitflag_2018{SQL_Injection_is_fun!}')")
conn.commit()
conn.close()
