from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Goods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cat = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    art = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return '{} {}'.format(self.cat, self.title)