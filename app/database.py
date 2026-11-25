"""Conexión a SQLite y creación del esquema."""
import os
import sqlite3

import click
from flask import current_app, g

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")


def get_db():
    """Devuelve la conexión de la petición actual (una por petición)."""
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def ensure_schema():
    """Crea la tabla si no existe (no borra datos)."""
    db = get_db()
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        db.executescript(f.read())
    db.commit()


def reset_db():
    """Borra y vuelve a crear la tabla, con datos de ejemplo."""
    db = get_db()
    db.execute("DROP TABLE IF EXISTS productos")
    ensure_schema()
    ejemplos = [
        ("Café de grano 1 kg", "Abarrotes", 289.00, 25, "Tostado medio, origen Veracruz"),
        ("Leche entera 1 L", "Lácteos", 28.50, 60, None),
        ("Vaso térmico 500 ml", "Accesorios", 199.90, 12, "Acero inoxidable"),
    ]
    db.executemany(
        "INSERT INTO productos (nombre, categoria, precio, stock, descripcion) VALUES (?, ?, ?, ?, ?)",
        ejemplos,
    )
    db.commit()


@click.command("init-db")
def init_db_command():
    """Reinicia la base de datos con productos de ejemplo."""
    reset_db()
    click.echo("Base de datos reiniciada con 3 productos de ejemplo.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
