from sw_app.db import db
from sw_app.catalog.models import Product

def add_data():
    test_data = [{'cat': 'Категория1', 'title': 'Название1', 'number': '45', 'articul': '123456', 'price': '4589',
                  'description': 'Описание1'},
                 {'cat': 'Категория2', 'title': 'Название2', 'number': '56', 'articul': '456987', 'price': '1025',
                  'description': 'Описание2'},
                 {'cat': 'Категория3', 'title': 'Название3', 'number': '99', 'articul': '754123', 'price': '7865',
                  'description': 'Описание3'}, ]
    for data in test_data:
        cat = data['cat']
        title = data['title']
        number = data['number']
        articul = data['articul']
        price = data['price']
        description = data['description']

        data_test(cat, title, number, articul, price, description)


def data_test(cat, title, number, articul, price, description):
    new_product = Product(cat=cat, title=title, number=number, articul=articul, price=price, description=description)
    db.session.add(new_product)
    db.session.commit()