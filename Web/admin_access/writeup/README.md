
# Admin Access

SQL injection hoo!
The server uses SQL queries in the form:

> "SELECT flag FROM users WHERE username = '{}' AND password = '{}'".format(username, password)


Try `admin' --` in username field.

