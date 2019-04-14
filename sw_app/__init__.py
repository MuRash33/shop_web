from flask import Flask
from sw_app.db import db
from sw_app.catalog.views import blueprint as catalog_blueprint
from sw_app.contact.views import blueprint as contact_blueprint
from sw_app.info.views import blueprint as info_blueprint
from sw_app.index.views import blueprint as index_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    app.register_blueprint(catalog_blueprint)
    app.register_blueprint(contact_blueprint)
    app.register_blueprint(info_blueprint)
    app.register_blueprint(index_blueprint)

<<<<<<< HEAD
=======
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
>>>>>>> 680f9b6532aeb464fd20921cc2d90eacdba0d345
    return app