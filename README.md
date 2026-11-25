# API REST de Inventario (Flask + SQLite)

Proyecto final de **Programación para Internet** — Universidad Anáhuac.
Autor: Rodrigo Valdespino Vertiz (00520621).

API REST para administrar el inventario de productos de un negocio local: crear, consultar, actualizar y eliminar productos guardados en una base de datos SQLite.

## Framework y dependencias

| Dependencia | Uso |
|---|---|
| Python 3.10+ | Lenguaje |
| Flask 3 | Framework web: rutas, peticiones y respuestas JSON |
| sqlite3 (biblioteca estándar) | Base de datos en un archivo (`instance/inventario.db`) |
| pytest | Pruebas automáticas (opcional) |

## Estructura

```
inventario-api/
├── run.py                  # Punto de entrada
├── requirements.txt
├── app/
│   ├── __init__.py         # Fábrica de la app (create_app), manejo de errores
│   ├── database.py         # Conexión SQLite y comando init-db
│   ├── schema.sql          # Tabla productos
│   ├── validators.py       # Validación de datos de entrada
│   └── routes/
│       └── productos.py    # Endpoints CRUD (Blueprint)
├── tests/test_api.py       # 10 pruebas automáticas
├── postman/                # Colección lista para importar en Postman
└── docs/                   # Documentación PDF y su generador
```

## Instalación

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt

flask --app run init-db      # crea la base con 3 productos de ejemplo
python run.py                # http://127.0.0.1:5000
```

Pruebas automáticas: `python -m pytest -v`

## Endpoints

Base: `http://127.0.0.1:5000/api`

| Método | Ruta | Descripción | Éxito |
|---|---|---|---|
| GET | `/health` | Estado de la API | 200 |
| POST | `/productos` | Crear producto | 201 |
| GET | `/productos` | Consultar todos (filtros `?categoria=` y `?buscar=`) | 200 |
| GET | `/productos/{id}` | Consultar por ID | 200 |
| PUT | `/productos/{id}` | Actualizar (reemplazo completo) | 200 |
| PATCH | `/productos/{id}` | Actualizar campos sueltos | 200 |
| DELETE | `/productos/{id}` | Eliminar | 200 |

Errores: `400` datos inválidos, `404` producto inexistente, `405` método no permitido.

### Ejemplo: crear

```http
POST /api/productos
Content-Type: application/json

{ "nombre": "Galletas de avena 300 g", "categoria": "Abarrotes", "precio": 35.5, "stock": 40 }
```

Respuesta `201 Created`:

```json
{ "id": 4, "nombre": "Galletas de avena 300 g", "categoria": "Abarrotes", "precio": 35.5,
  "stock": 40, "descripcion": null, "creado_en": "2026-11-25 12:10:00", "actualizado_en": "2026-11-25 12:10:00" }
```

## Postman

Importa `postman/Inventario_API.postman_collection.json` y ejecuta las peticiones en orden.

## Ver los cambios en la base de datos

```bash
sqlite3 instance/inventario.db "SELECT * FROM productos;"
```

También puede abrirse `instance/inventario.db` con DB Browser for SQLite o con la extensión SQLite Viewer de VS Code.
