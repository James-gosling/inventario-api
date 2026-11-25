"""Fábrica de la aplicación Flask para la API REST de Inventario."""
import os

from flask import Flask, jsonify

from . import database
from .routes.productos import productos_bp


def create_app(config=None):
    """Crea y configura la aplicación Flask."""
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, "inventario.db"),
    )
    if config:
        app.config.update(config)

    # JSON legible: respeta el orden de los campos y los acentos
    app.json.sort_keys = False
    app.json.ensure_ascii = False

    os.makedirs(app.instance_path, exist_ok=True)

    # Base de datos: cierre de conexión y comando `flask --app run init-db`
    database.init_app(app)

    # Rutas
    app.register_blueprint(productos_bp, url_prefix="/api/productos")

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok", "servicio": "API de Inventario"})

    # Respuestas de error en JSON (en lugar de páginas HTML)
    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"error": "Recurso no encontrado"}), 404

    @app.errorhandler(405)
    def method_not_allowed(_error):
        return jsonify({"error": "Método HTTP no permitido para esta ruta"}), 405

    @app.errorhandler(500)
    def server_error(_error):
        return jsonify({"error": "Error interno del servidor"}), 500

    # Crea las tablas la primera vez que se ejecuta
    with app.app_context():
        database.ensure_schema()

    return app
