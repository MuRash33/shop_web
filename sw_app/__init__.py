from flask import Flask, render_template
from sw_app.models import db, Goods


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/goods')
    def goods():
        catal = Goods.query.order_by(Goods.title).all()
        return render_template('goods.html', catal=catal)

    @app.route('/contacts')
    def contacts():
        return render_template('contacts.html')

    @app.route('/info')
    def info():
        return render_template('info.html')
    return app