from sw_app import create_app
from testcont import adata

app = create_app()
with app.app_context():
    adata()