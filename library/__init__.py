# External modules
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import psycopg2

app = Flask(__name__)

app.config['SECRET_KEY'] = 'redwire'

os.environ['SQL_DATABASE_URL'] = 'postgresql://postgres:ilovedata@localhost/Redwire'

ENV = 'dev'

if ENV == 'dev':
    # Use the PostgreSQL URL with your credentials
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:ilovedata@localhost/Redwire'
    app.config['SECRET_KEY'] = 'redwire'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQL_DATABASE_URL']  # Set this in your environment
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']  # Set this in your environment

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from library.routes import routes, book_routes, member_routes, transaction_routes
