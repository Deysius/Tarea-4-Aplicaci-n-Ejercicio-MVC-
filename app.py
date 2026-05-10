from flask import Flask
from utils.database import db
from flask_migrate import Migrate
import os
import sqlite3

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'dev')

db.init_app(app)
Migrate(app, db)

from controllers.venta_controller import main_blueprint
app.register_blueprint(main_blueprint)

def init_db():
    db_path = os.path.join(app.instance_path, 'db.sqlite3')

    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)

    if not os.path.exists(db_path):
        with sqlite3.connect(db_path) as conn:
            with open('data.sql', encoding='utf-8') as f:
                conn.executescript(f.read())
                print("Base de datos creada con datos iniciales ✅")

with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run(debug=True)