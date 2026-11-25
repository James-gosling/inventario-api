"""Endpoints CRUD del recurso /api/productos."""
from flask import Blueprint, jsonify, request, url_for

from ..database import get_db
from ..validators import validar_producto

productos_bp = Blueprint("productos", __name__)


def _a_dict(row):
    return dict(row) if row is not None else None


def _buscar(producto_id):
    return get_db().execute("SELECT * FROM productos WHERE id = ?", (producto_id,)).fetchone()


def _no_encontrado(producto_id):
    return jsonify({"error": f"No existe un producto con id {producto_id}"}), 404


def _leer_json():
    data = request.get_json(silent=True)
    if data is None:
        return None, (jsonify({"error": "El cuerpo debe ser JSON válido (Content-Type: application/json)"}), 400)
    return data, None


# ---------- CREAR ----------
@productos_bp.post("")
def crear_producto():
    data, error = _leer_json()
    if error:
        return error
    limpio, errores = validar_producto(data)
    if errores:
        return jsonify({"error": "Datos inválidos", "detalles": errores}), 400

    db = get_db()
    cur = db.execute(
        "INSERT INTO productos (nombre, categoria, precio, stock, descripcion) VALUES (?, ?, ?, ?, ?)",
        (limpio["nombre"], limpio["categoria"], limpio["precio"],
         limpio.get("stock", 0), limpio.get("descripcion")),
    )
    db.commit()
    producto = _a_dict(_buscar(cur.lastrowid))
    resp = jsonify(producto)
    resp.status_code = 201
    resp.headers["Location"] = url_for("productos.obtener_producto", producto_id=producto["id"])
    return resp


# ---------- CONSULTAR TODOS ----------
@productos_bp.get("")
def listar_productos():
    """Filtros opcionales: ?categoria=Lácteos  ?buscar=café"""
    consulta = "SELECT * FROM productos"
    condiciones, params = [], []

    categoria = request.args.get("categoria")
    if categoria:
        condiciones.append("categoria = ?")
        params.append(categoria)

    buscar = request.args.get("buscar")
    if buscar:
        condiciones.append("nombre LIKE ?")
        params.append(f"%{buscar}%")

    if condiciones:
        consulta += " WHERE " + " AND ".join(condiciones)
    consulta += " ORDER BY id"

    filas = get_db().execute(consulta, params).fetchall()
    productos = [_a_dict(f) for f in filas]
    return jsonify({"total": len(productos), "productos": productos})


# ---------- CONSULTAR POR ID ----------
@productos_bp.get("/<int:producto_id>")
def obtener_producto(producto_id):
    producto = _buscar(producto_id)
    if producto is None:
        return _no_encontrado(producto_id)
    return jsonify(_a_dict(producto))


# ---------- ACTUALIZAR ----------
def _actualizar(producto_id, parcial):
    if _buscar(producto_id) is None:
        return _no_encontrado(producto_id)
    data, error = _leer_json()
    if error:
        return error
    limpio, errores = validar_producto(data, parcial=parcial)
    if errores:
        return jsonify({"error": "Datos inválidos", "detalles": errores}), 400

    if not parcial:
        # PUT reemplaza el recurso: los opcionales que no vengan vuelven a su valor por defecto
        limpio.setdefault("stock", 0)
        limpio.setdefault("descripcion", None)

    asignaciones = ", ".join(f"{campo} = ?" for campo in limpio)
    db = get_db()
    db.execute(
        f"UPDATE productos SET {asignaciones}, actualizado_en = datetime('now', 'localtime') WHERE id = ?",
        (*limpio.values(), producto_id),
    )
    db.commit()
    return jsonify(_a_dict(_buscar(producto_id)))


@productos_bp.put("/<int:producto_id>")
def reemplazar_producto(producto_id):
    return _actualizar(producto_id, parcial=False)


@productos_bp.patch("/<int:producto_id>")
def modificar_producto(producto_id):
    return _actualizar(producto_id, parcial=True)


# ---------- ELIMINAR ----------
@productos_bp.delete("/<int:producto_id>")
def eliminar_producto(producto_id):
    if _buscar(producto_id) is None:
        return _no_encontrado(producto_id)
    db = get_db()
    db.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
    db.commit()
    return jsonify({"mensaje": f"Producto {producto_id} eliminado correctamente"})
