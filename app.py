from flask import Flask
from models import db
import os

app = Flask(__name__)

os.makedirs('data', exist_ok=True)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{
    os.path.join(basedir, "data", "movi.db")}'
db.init_app(app)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
