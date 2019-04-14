from flask import Blueprint, render_template

blueprint = Blueprint('contacts', __name__)



@blueprint.route('/contacts')
def contacts():
    page_title = 'Контакты'
    return render_template('contact/contacts.html', page_title=page_title)