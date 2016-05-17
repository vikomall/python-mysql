import json
import os

from flask import Flask, render_template
from flask.ext.mysql import MySQL
from flask import request

app = Flask(__name__)
mysql = MySQL()
def get_db_connection():
    # Get DB info from environment
    db = os.environ.get("DATABASE", None) or os.environ.get("database", None)
    username = os.environ.get("USERNAME", None) or os.environ.get("username", None)
    password = os.environ.get("PASSWORD", None) or os.environ.get("password", None)
    hostname = os.environ.get("DBHOST", None) or os.environ.get("dbhost", None)
    if db is None or username is None or password is None or hostname is None:
        raise Exception("some env info missing")
    
    app.config['MYSQL_DATABASE_DB'] = db
    app.config['MYSQL_DATABASE_HOST'] = hostname
    app.config['MYSQL_DATABASE_USER'] = username
    app.config['MYSQL_DATABASE_PASSWORD'] = password
    mysql.init_app(app)
    conn = mysql.connect()
    return conn

try:
    conn = get_db_connection()
except Exception as exp:
    conn = None

@app.route("/")
def hello():
    if conn is None:
        return "database connection string is not provided %s" % str(exp)

    cur = conn.cursor()
    cur.execute("SELECT title, content FROM posts")
    entries = [dict(title=row[0], content=row[1]) for row in cur.fetchall()]
    return render_template('index.html', entries=entries)

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=80)
