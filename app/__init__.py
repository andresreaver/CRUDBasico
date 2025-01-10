from flask import Flask
from .routes import register_routes
from .database import create_tables

def create_app():
    app = Flask(__name__)

    #Crear las tablas enla base de datos si no existen
    create_tables()

    #Rgistrar las rutas
    register_routes(app)

    return app