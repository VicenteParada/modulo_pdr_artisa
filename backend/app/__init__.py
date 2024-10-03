from flask import Flask
from .config import Config

def create_app():
    # Crear la instancia de la aplicación
    app = Flask(__name__)
    
    # Cargar la configuración desde el archivo de configuración
    app.config.from_object(Config)

    # Inicializar extensiones aquí (ejemplo: bases de datos, migraciones)
    # from flask_sqlalchemy import SQLAlchemy
    # db = SQLAlchemy(app)

    # Registrar rutas
    with app.app_context():
        from .routes import main as main_routes
        app.register_blueprint(main_routes)

    return app
