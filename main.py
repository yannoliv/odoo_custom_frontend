"""
Simple module to show how to connect to a odoo database
"""


from flask import Flask, render_template
import psycopg2
import psycopg2.extras
from config import config

app = Flask(__name__)


def connect() -> list[dict]:
    """
    Database connect
    :return: List of dictionaries of the objects
    """
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""
        SELECT name,quantity,id 
        FROM product_template 
        WHERE quantity IS NOT NULL
        LIMIT 30
    """)
    res = [dict(record) for record in cur]
    cur.close()
    return res


@app.route("/")
def index():
    res = connect()
    # /web/image?model=product.template&id=85&field=image_256
    return render_template('index.html', lines=res)
