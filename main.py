from flask import Flask
import psycopg2
from config import config

app = Flask(__name__)


def connect():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    cur.execute('SELECT * from product_template')
    line = cur.fetchone()
    cur.close()
    return line

@app.route("/")
def index():
    line = connect()

    return f'{line}'
