from flask import Blueprint, render_template

blueprint = Blueprint('index', __name__)

@blueprint.route('/')
def index():
    page_title = 'Главная'
    return render_template('index/index.html', page_title=page_title)
