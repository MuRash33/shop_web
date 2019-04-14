import xml.dom.minidom
from sw_app.db import db
from sw_app.catalog.models import Product

def adata():
    dom = xml.dom.minidom.parse('5.xml')
    dom.normalize()

    item = dom.getElementsByTagName("item")
    for i in item:
        articul = (i.getElementsByTagName('oe')[0]).childNodes[0].nodeValue
        price = (i.getElementsByTagName('pr_exp')[0]).childNodes[0].nodeValue
        try:
            number = (i.getElementsByTagName('kolvo')[0]).childNodes[0].nodeValue
        except:
            number = 'Нет в наличии'
        name = dom.getElementsByTagName('name')
        for title in name:
            title = (i.getElementsByTagName('name')[0]).childNodes[0].nodeValue
        add_base(articul, price, title, number)

def add_base(articul, price, title, number):
    add_poduct = Product(articul=articul, price=price, title=title, number=number)
    db.session.add(add_poduct)
    db.session.commit()


