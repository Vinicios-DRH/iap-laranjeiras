from src import database
from src import app

with app.app_context():
    database.create_all()