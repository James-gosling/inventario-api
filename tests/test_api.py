"""Pruebas automáticas del CRUD. Ejecutar con: python -m pytest -v"""
import pytest

from app import create_app
from app.database import reset_db


@pytest.fixture
def client(tmp_path):
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "test.db")})
    with app.app_context():
        reset_db()
    return app.test_client()


NUEVO = {"nombre": "Galletas de avena", "categoria": "Abarrotes", "precio": 35.5, "stock": 40}


def test_health(client):
    assert client.get("/api/health").status_code == 200


def test_listar(client):
    r = client.get("/api/productos")
    assert r.status_code == 200
    assert r.get_json()["total"] == 3


def test_crear_y_consultar(client):
    r = client.post("/api/productos", json=NUEVO)
    assert r.status_code == 201
    nuevo = r.get_json()
    assert nuevo["id"] == 4 and nuevo["nombre"] == "Galletas de avena"
    assert r.headers["Location"].endswith("/api/productos/4")
    assert client.get("/api/productos/4").get_json()["stock"] == 40


def test_crear_invalido(client):
    r = client.post("/api/productos", json={"nombre": "", "precio": -3})
    assert r.status_code == 400
    detalles = r.get_json()["detalles"]
    assert {"nombre", "categoria", "precio"} <= set(detalles)


def test_crear_sin_json(client):
    r = client.post("/api/productos", data="hola", content_type="text/plain")
    assert r.status_code == 400


def test_consultar_inexistente(client):
    assert client.get("/api/productos/999").status_code == 404


def test_actualizar_put(client):
    r = client.put("/api/productos/1", json={"nombre": "Café 500 g", "categoria": "Abarrotes", "precio": 159})
    assert r.status_code == 200
    p = r.get_json()
    assert p["nombre"] == "Café 500 g" and p["precio"] == 159 and p["stock"] == 0


def test_actualizar_patch(client):
    r = client.patch("/api/productos/2", json={"stock": 5})
    assert r.status_code == 200
    p = r.get_json()
    assert p["stock"] == 5 and p["nombre"] == "Leche entera 1 L"


def test_eliminar(client):
    assert client.delete("/api/productos/3").status_code == 200
    assert client.get("/api/productos/3").status_code == 404
    assert client.delete("/api/productos/3").status_code == 404


def test_filtros(client):
    r = client.get("/api/productos?categoria=Lácteos")
    assert r.get_json()["total"] == 1
    r = client.get("/api/productos?buscar=café")
    assert r.get_json()["total"] == 1
