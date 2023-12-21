from flask import Flask, request, g
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATABASE = 'database.sqlite'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def is_valid_input(input_str):
    """Check if the input is valid and does not contain SQL injection risk."""
    disallowed_keywords = [ 'DROP', 'DELETE', 'ALTER', 'INSERT', 'UPDATE', 'SELECT', 'EXEC', 'UNION']
    if any(keyword in input_str.upper() for keyword in disallowed_keywords):
        return False
    return True

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return "Welcome to the SQL Injection Vulnerable Server!"

@app.route('/api/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Input validation
    if not is_valid_input(username) or not is_valid_input(password):
        return "Naughty naughty!"

    cur = get_db().cursor()
    query = "SELECT flag FROM users WHERE username = '{}' AND password = '{}'".format(username, password)
    cur.execute(query)
    result = cur.fetchone()
    
    
    if result:
        return "Login successful! Flag: {}".format(result[0])
    else:
        return "Login failed!"

if __name__ == '__main__':
    app.run(debug=True)
