from flask import Flask, render_template, redirect, url_for
from config import config
import xmlrpc.client
import logging
import itertools

app = Flask(__name__)


class OdooDatabase:
    def __init__(self):
        params = config()
        common = xmlrpc.client.ServerProxy(f"{params['host']}/xmlrpc/2/common")
        self.db, self.user, self.password = params['database'], params['user'], params['password']
        self.uid = common.authenticate(self.db, self.user, self.password, {})
        self.models = xmlrpc.client.ServerProxy(f"{params['host']}/xmlrpc/2/object")

    def execute(self, *args):
        return self.models.execute_kw(self.db, self.uid, self.password, *args)


@app.route("/")
def index():
    try:
        odoo = OdooDatabase()
    except ConnectionRefusedError as e:
        logging.warning(f'There is no connection to the odoo server: {e}')
        return redirect(url_for('not_found'))

    fields_products = ['id', 'name', 'quantity', 'categ_id']
    products_list = odoo.execute('product.template', 'search_read', [[['image_256', '!=', '']]],
                         {'fields': fields_products})
    print(products_list[0])

    fields_categories = ['id', 'filter_category', 'name']
    categories = odoo.execute('product.public.category', 'search_read',
                              [[['company_id', '=', 1], ['filter_category', '!=', False]]],
                              {'fields': fields_categories, 'order': 'filter_category'})
    categories = itertools.groupby(categories, lambda x: x['filter_category'])
    categories = [{'name': k.capitalize(), 'categories': list(g)} for k, g in categories]
    print(categories[0])

    return render_template('index.html', env={'products_list': products_list, 'categories': categories})


@app.route("/not-found")
def not_found():
    return render_template('error.html')
