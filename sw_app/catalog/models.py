from sw_app.db import db
from flask import Blueprint

blueprint = Blueprint('catalog', __name__)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cat = db.Column(db.String, nullable=True)
    title = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    articul = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)


    def __repr__(self):
        return '{}'.format(self.cat)