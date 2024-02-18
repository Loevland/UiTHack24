> # Admin Access
> > Web - 337pts/33 solves
>
> You have to inflitraite the admin area of this website to get the flag. But how do you access it?

## Writeup
SQL injection hoo!
The server uses SQL queries in the form:

> "SELECT flag FROM users WHERE username = '{}' AND password = '{}'".format(username, password)


Try `admin' --` in username field to get the flag.