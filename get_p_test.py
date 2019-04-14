from sw_app import create_app
from test_db import add_data

app = create_app()
with app.app_context():
    add_data()