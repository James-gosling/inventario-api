"""Validación de los datos de entrada de un producto."""

CAMPOS = ("nombre", "categoria", "precio", "stock", "descripcion")
OBLIGATORIOS = ("nombre", "categoria", "precio")


def validar_producto(data, parcial=False):
    """Valida el JSON recibido.

    parcial=False -> creación o reemplazo (PUT): los campos obligatorios deben venir.
    parcial=True  -> actualización parcial (PATCH): solo se validan los que vengan.

    Devuelve (datos_limpios, errores).
    """
    if not isinstance(data, dict):
        return None, {"cuerpo": "Se esperaba un objeto JSON"}

    errores = {}
    limpio = {}

    desconocidos = set(data) - set(CAMPOS)
    if desconocidos:
        errores["campos_desconocidos"] = sorted(desconocidos)

    if not parcial:
        for campo in OBLIGATORIOS:
            if campo not in data:
                errores[campo] = "Campo obligatorio"

    if "nombre" in data:
        nombre = data["nombre"]
        if not isinstance(nombre, str) or not nombre.strip():
            errores["nombre"] = "Debe ser un texto no vacío"
        elif len(nombre.strip()) > 120:
            errores["nombre"] = "Máximo 120 caracteres"
        else:
            limpio["nombre"] = nombre.strip()

    if "categoria" in data:
        categoria = data["categoria"]
        if not isinstance(categoria, str) or not categoria.strip():
            errores["categoria"] = "Debe ser un texto no vacío"
        else:
            limpio["categoria"] = categoria.strip()

    if "precio" in data:
        precio = data["precio"]
        if isinstance(precio, bool) or not isinstance(precio, (int, float)) or precio < 0:
            errores["precio"] = "Debe ser un número mayor o igual a 0"
        else:
            limpio["precio"] = round(float(precio), 2)

    if "stock" in data:
        stock = data["stock"]
        if isinstance(stock, bool) or not isinstance(stock, int) or stock < 0:
            errores["stock"] = "Debe ser un entero mayor o igual a 0"
        else:
            limpio["stock"] = stock

    if "descripcion" in data:
        descripcion = data["descripcion"]
        if descripcion is not None and not isinstance(descripcion, str):
            errores["descripcion"] = "Debe ser texto o null"
        else:
            limpio["descripcion"] = descripcion.strip() if isinstance(descripcion, str) else None

    if parcial and not limpio and not errores:
        errores["cuerpo"] = "No se envió ningún campo para actualizar"

    return limpio, errores
