from flask import Blueprint, render_template
from sw_app.catalog.models import Product

blueprint = Blueprint('catalog', __name__)

@blueprint.route('/product')
def product():
    page_title = 'Товары'
    catal = Product.query.all()
    return render_template('product/product.html', catal=catal, page_title=page_title)