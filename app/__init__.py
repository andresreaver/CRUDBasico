from flask import Flask

from .database import create_tables
from .routes import register_routes


def create_app():
    app = Flask(__name__)

    #Crear las tablas en la base de datos si no existen
    create_tables()

    #Rgistrar las rutas
    register_routes(app)

    return app