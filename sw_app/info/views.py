from flask import Blueprint, render_template

blueprint = Blueprint('info', __name__)

@blueprint.route('/info')
def info():
    page_title = 'О Компании'
    return render_template('info/info.html', page_title=page_title)