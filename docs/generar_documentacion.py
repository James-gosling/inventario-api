"""Genera docs/Documentacion_API_Inventario.pdf

Uso:
    pip install reportlab
    python docs/generar_documentacion.py

Las capturas de Postman se toman de docs/capturas/ con estos nombres
(si una no existe, se deja un recuadro indicando cuál falta):
    01_crear.png  02_listar.png  03_por_id.png  04_put.png
    05_patch.png  06_eliminar.png  07_error_404.png  08_error_400.png
    09_base_de_datos.png  10_pytest.png
También se aceptan .jpg. Edita VIDEO_URL y REPO_URL antes de generar.
"""
import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (BaseDocTemplate, Frame, Image, KeepTogether, NextPageTemplate,
                                PageBreak, PageTemplate, Paragraph, Preformatted, Spacer, Table,
                                TableStyle)

# ------------------------------------------------------------------ datos editables
VIDEO_URL = "[pega aquí la liga de YouTube (no listado)]"
REPO_URL = "[pega aquí la liga del repositorio de GitHub o indica: archivo .zip adjunto]"
FECHA = "25 de noviembre de 2026"
# ----------------------------------------------------------------------------------

AQUI = os.path.dirname(os.path.abspath(__file__))
CAPTURAS = os.path.join(AQUI, "capturas")
SALIDA = os.path.join(AQUI, "Documentacion_API_Inventario.pdf")

NARANJA = colors.HexColor("#D9601E")
AZUL = colors.HexColor("#1F2A44")
GRIS = colors.HexColor("#555555")
FONDO = colors.HexColor("#F4F2EE")

W, H = letter
M = 2.5 * cm
ANCHO = W - 2 * M


def decor(c, doc):
    c.saveState()
    c.setStrokeColor(NARANJA)
    c.setLineWidth(0.8)
    c.line(M, H - 1.6 * cm, W - M, H - 1.6 * cm)
    c.setFont("Times-Italic", 9)
    c.setFillColor(GRIS)
    c.drawString(M, H - 1.4 * cm, "Programación para Internet · Proyecto final: API REST")
    c.drawRightString(W - M, H - 1.4 * cm, "Universidad Anáhuac")
    c.line(M, 1.8 * cm, W - M, 1.8 * cm)
    c.setFont("Times-Roman", 9)
    c.drawString(M, 1.3 * cm, "Rodrigo Valdespino Vertiz · 00520621")
    c.drawRightString(W - M, 1.3 * cm, f"Página {doc.page}")
    c.restoreState()


def portada(c, doc):
    c.saveState()
    c.setStrokeColor(NARANJA)
    c.setLineWidth(2)
    c.line(M, H - 3 * cm, W - M, H - 3 * cm)
    c.line(M, 3 * cm, W - M, 3 * cm)
    c.restoreState()


cuerpo = ParagraphStyle("c", fontName="Times-Roman", fontSize=12, leading=17,
                        alignment=TA_JUSTIFY, spaceAfter=7)
h1 = ParagraphStyle("h1", fontName="Times-Bold", fontSize=14, leading=19,
                    textColor=AZUL, spaceBefore=12, spaceAfter=6)
h2 = ParagraphStyle("h2", fontName="Times-BoldItalic", fontSize=12, leading=16,
                    spaceBefore=6, spaceAfter=4)
celda = ParagraphStyle("t", fontName="Times-Roman", fontSize=10.5, leading=13)
celda_b = ParagraphStyle("tb", parent=celda, fontName="Times-Bold", textColor=colors.white)
pie = ParagraphStyle("pie", fontName="Times-Italic", fontSize=10, leading=13,
                     alignment=TA_CENTER, textColor=GRIS, spaceAfter=10)
codigo = ParagraphStyle("code", fontName="Courier", fontSize=9, leading=11.5)
ref = ParagraphStyle("r", fontName="Times-Roman", fontSize=12, leading=17, alignment=TA_LEFT,
                     leftIndent=1.27 * cm, firstLineIndent=-1.27 * cm, spaceAfter=6)
pc = ParagraphStyle("pc", fontName="Times-Roman", fontSize=13, leading=20, alignment=TA_CENTER)
pcb = ParagraphStyle("pcb", parent=pc, fontName="Times-Bold", fontSize=15, textColor=AZUL)
pct = ParagraphStyle("pct", parent=pc, fontName="Times-Bold", fontSize=20, leading=28)
bullet = ParagraphStyle("b", parent=cuerpo, leftIndent=0.8 * cm, bulletIndent=0.3 * cm,
                        spaceAfter=3, alignment=TA_LEFT)

s = []


def P(t):
    s.append(Paragraph(t, cuerpo))


def B(t):
    s.append(Paragraph(t, bullet, bulletText="•"))


def code(txt):
    t = Table([[Preformatted(txt.strip("\n"), codigo)]], colWidths=[ANCHO])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), FONDO),
                           ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#CFCAC0")),
                           ("LEFTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 6),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    s.append(t)
    s.append(Spacer(1, 8))


def tabla(filas, anchos):
    data = [[Paragraph(str(x), celda_b if i == 0 else celda) for x in fila]
            for i, fila in enumerate(filas)]
    t = Table(data, colWidths=anchos, repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), AZUL),
                           ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#B9B4AA")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, FONDO])]))
    s.append(t)
    s.append(Spacer(1, 10))


def captura(nombre, figura, texto):
    ruta = None
    for ext in (".png", ".jpg", ".jpeg"):
        p = os.path.join(CAPTURAS, nombre + ext)
        if os.path.exists(p):
            ruta = p
            break
    if ruta:
        iw, ih = ImageReader(ruta).getSize()
        ancho = ANCHO
        alto = ancho * ih / iw
        if alto > 11 * cm:
            alto = 11 * cm
            ancho = alto * iw / ih
        img = Image(ruta, width=ancho, height=alto)
    else:
        img = Table([[Paragraph(f"[Captura pendiente: guardar como <b>docs/capturas/{nombre}.png</b>]",
                                ParagraphStyle("ph", parent=celda, alignment=TA_CENTER, textColor=GRIS))]],
                    colWidths=[ANCHO], rowHeights=[4 * cm])
        img.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.8, NARANJA),
                                 ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    s.append(KeepTogether([img, Spacer(1, 4),
                           Paragraph(f"<b>Figura {figura}.</b> {texto}", pie)]))


# ================================================================== PORTADA
s += [Spacer(1, 1.2 * cm),
      Paragraph("Universidad Anáhuac", pcb),
      Paragraph("Red de Universidades Anáhuac", pc),
      Spacer(1, 0.4 * cm),
      Paragraph("Ingeniería en Tecnologías de la Información y Negocios Digitales", pc),
      Spacer(1, 2.0 * cm),
      Paragraph("API REST de Inventario", pct),
      Paragraph("Documentación técnica del proyecto", pc),
      Spacer(1, 0.4 * cm),
      Paragraph("Proyecto final: Desarrollo y presentación de una API REST", pc),
      Spacer(1, 2.0 * cm),
      Paragraph("<b>Alumno:</b> Rodrigo Valdespino Vertiz", pc),
      Paragraph("<b>Matrícula:</b> 00520621", pc),
      Spacer(1, 0.3 * cm),
      Paragraph("<b>Materia:</b> Programación para Internet (202660_92615)", pc),
      Paragraph("<b>Profesora:</b> Mtra. Karla Vianney Ramos García", pc),
      Spacer(1, 1.8 * cm),
      Paragraph(FECHA, pc),
      NextPageTemplate("normal"), PageBreak()]

# ================================================================== 1. INTRODUCCIÓN
s.append(Paragraph("1. Introducción", h1))
P("Este proyecto consiste en una API REST para administrar el inventario de productos de un negocio "
  "local (por ejemplo, una tienda de abarrotes o una cafetería). La API permite registrar productos, "
  "consultarlos todos o por su identificador, actualizar sus datos y eliminarlos. La información se "
  "guarda en una base de datos SQLite, por lo que los cambios se conservan aunque el servidor se reinicie.")
P("REST (<i>Representational State Transfer</i>) es un estilo de arquitectura propuesto por Fielding (2000) "
  "en el que cada recurso se identifica con una URL y se manipula con los métodos estándar de HTTP. En esta "
  "API el recurso es <b>producto</b>, disponible en <font face='Courier'>/api/productos</font>, y cada "
  "operación CRUD corresponde a un método HTTP con la semántica que define el estándar (Fielding et al., 2022).")
tabla([["Operación", "Método HTTP", "Ruta", "Código de éxito"],
       ["Crear", "POST", "/api/productos", "201 Created"],
       ["Consultar todos", "GET", "/api/productos", "200 OK"],
       ["Consultar por ID", "GET", "/api/productos/{id}", "200 OK"],
       ["Actualizar", "PUT / PATCH", "/api/productos/{id}", "200 OK"],
       ["Eliminar", "DELETE", "/api/productos/{id}", "200 OK"]],
      [3.6 * cm, 3 * cm, 5 * cm, ANCHO - 11.6 * cm])
s.append(Paragraph("Repositorio y video", h2))
B(f"<b>Proyecto:</b> {REPO_URL}")
B(f"<b>Video de demostración:</b> {VIDEO_URL}")

# ================================================================== 2. FRAMEWORK
s.append(Paragraph("2. Framework utilizado: Flask", h1))
P("Se eligió <b>Flask 3</b>, un microframework de Python mantenido por la organización Pallets. Flask "
  "proporciona lo esencial para construir aplicaciones web (enrutamiento, manejo de peticiones y "
  "respuestas, y serialización a JSON) y deja que el desarrollador decida el resto de componentes "
  "(Pallets, 2025). Las razones de la elección fueron:")
B("Poco código para lograr una API completa, lo que facilita explicar el proyecto en un video corto.")
B("Python es el lenguaje que más utilizo, así que el tiempo se dedicó al diseño de la API y no a la sintaxis.")
B("Permite organizar la aplicación con el patrón <i>application factory</i> y <i>Blueprints</i>, "
  "recomendado para proyectos que crecen (Grinberg, 2018).")
B("Incluye un cliente de pruebas que permite automatizar la verificación del CRUD con pytest.")
P("Como motor de base de datos se usó <b>SQLite</b>, que guarda toda la base en un solo archivo y no "
  "requiere instalar un servidor. Su documentación lo recomienda para aplicaciones de bajo y mediano "
  "tráfico, prototipos y entornos de desarrollo (SQLite, s.f.), que es justo el alcance de este proyecto.")

# ================================================================== 3. ARQUITECTURA
s.append(Paragraph("3. Arquitectura del proyecto", h1))
P("La API sigue una arquitectura en capas: cada capa tiene una sola responsabilidad y solo se comunica con "
  "la siguiente. Así, si en el futuro se cambia SQLite por MySQL o PostgreSQL, solo se modifica la capa de datos.")
capas = [["Capa", "Archivo", "Responsabilidad"],
         ["Cliente", "Postman / navegador", "Envía peticiones HTTP con cuerpo JSON."],
         ["Aplicación", "app/__init__.py", "Crea la app (create_app), registra rutas y responde errores 404/405/500 en JSON."],
         ["Rutas (controlador)", "app/routes/productos.py", "Blueprint con los endpoints CRUD; traduce cada petición en una operación."],
         ["Validación", "app/validators.py", "Revisa tipos y valores (precio y stock no negativos, campos obligatorios)."],
         ["Datos", "app/database.py · schema.sql", "Abre una conexión SQLite por petición, crea la tabla y carga datos de ejemplo."],
         ["Persistencia", "instance/inventario.db", "Archivo de la base de datos SQLite."]]
tabla(capas, [3.4 * cm, 4.6 * cm, ANCHO - 8 * cm])
s.append(Paragraph("Flujo de una petición", h2))
code("""
Postman --HTTP/JSON--> Flask (run.py) --> Blueprint /api/productos --> validators.py
                                                     |
                                                     v
Postman <--JSON + código HTTP-- respuesta <-- database.py --> SQLite (inventario.db)
""")
s.append(Paragraph("Estructura de carpetas", h2))
code("""
inventario-api/
|-- run.py                      Punto de entrada (python run.py)
|-- requirements.txt            Dependencias
|-- README.md                   Guía rápida
|-- app/
|   |-- __init__.py             Fábrica de la aplicación y manejo de errores
|   |-- database.py             Conexión SQLite y comando init-db
|   |-- schema.sql              Definición de la tabla productos
|   |-- validators.py           Validación de datos de entrada
|   `-- routes/
|       `-- productos.py        Endpoints CRUD
|-- tests/test_api.py           10 pruebas automáticas (pytest)
|-- postman/                    Colección de Postman lista para importar
`-- docs/                       Esta documentación y su generador
""")
s.append(Paragraph("Modelo de datos: tabla productos", h2))
tabla([["Campo", "Tipo", "Regla"],
       ["id", "INTEGER", "Llave primaria autoincremental"],
       ["nombre", "TEXT", "Obligatorio, máximo 120 caracteres"],
       ["categoria", "TEXT", "Obligatorio"],
       ["precio", "REAL", "Obligatorio, mayor o igual a 0"],
       ["stock", "INTEGER", "Entero mayor o igual a 0 (0 por defecto)"],
       ["descripcion", "TEXT", "Opcional"],
       ["creado_en / actualizado_en", "TEXT", "Fecha y hora asignadas automáticamente"]],
      [5 * cm, 2.6 * cm, ANCHO - 7.6 * cm])

# ================================================================== 4. DEPENDENCIAS
s.append(Paragraph("4. Dependencias principales", h1))
tabla([["Dependencia", "Versión", "Uso en el proyecto"],
       ["Python", "3.10 o superior", "Lenguaje de programación"],
       ["Flask", "3.x", "Framework web: rutas, peticiones, respuestas JSON y CLI"],
       ["sqlite3", "Biblioteca estándar", "Acceso a la base de datos SQLite (no requiere instalación)"],
       ["pytest", "8.x", "Pruebas automáticas del CRUD (dependencia de desarrollo)"],
       ["Postman", "Aplicación de escritorio", "Pruebas manuales de los endpoints"]],
      [3.2 * cm, 3.6 * cm, ANCHO - 6.8 * cm])

# ================================================================== 5. INSTALACIÓN
s.append(Paragraph("5. Instalación y ejecución", h1))
P("1. Clonar el repositorio (o descomprimir el .zip) y entrar a la carpeta del proyecto.")
P("2. Crear y activar un entorno virtual, e instalar las dependencias:")
code("""
python -m venv .venv
.venv\\Scripts\\activate          # Windows
source .venv/bin/activate         # Linux / macOS
pip install -r requirements.txt
""")
P("3. Crear la base de datos con tres productos de ejemplo y levantar el servidor:")
code("""
flask --app run init-db
python run.py
 * Running on http://127.0.0.1:5000
""")
s.append(Paragraph("4. Importar en Postman el archivo <font face='Courier'>postman/Inventario_API.postman_collection.json</font>. "
  "La colección usa la variable <font face='Courier'>{{baseUrl}}</font> y guarda automáticamente el id del "
  "producto creado en <font face='Courier'>{{productoId}}</font>, para que las peticiones siguientes "
  "trabajen sobre ese producto.", ParagraphStyle("izq", parent=cuerpo, alignment=TA_LEFT)))

# ================================================================== 6. ENDPOINTS
s.append(Paragraph("6. Ejemplos de endpoints", h1))
P("Todas las rutas parten de <font face='Courier'>http://127.0.0.1:5000/api</font>. Las peticiones que envían "
  "datos deben incluir el encabezado <font face='Courier'>Content-Type: application/json</font>.")

s.append(Paragraph("6.1 Crear producto: POST /productos", h2))
code("""
{
  "nombre": "Galletas de avena 300 g",
  "categoria": "Abarrotes",
  "precio": 35.50,
  "stock": 40,
  "descripcion": "Paquete individual"
}
""")
P("Respuesta <b>201 Created</b> (incluye el encabezado <font face='Courier'>Location: /api/productos/4</font>):")
code("""
{
  "id": 4,
  "nombre": "Galletas de avena 300 g",
  "categoria": "Abarrotes",
  "precio": 35.5,
  "stock": 40,
  "descripcion": "Paquete individual",
  "creado_en": "2026-11-25 12:10:12",
  "actualizado_en": "2026-11-25 12:10:12"
}
""")
s.append(Paragraph("6.2 Consultar todos: GET /productos", h2))
P("Devuelve el total y la lista de productos. Acepta filtros opcionales: "
  "<font face='Courier'>?categoria=Lácteos</font> y <font face='Courier'>?buscar=café</font>.")
code("""
{ "total": 4, "productos": [ { "id": 1, "nombre": "Café de grano 1 kg", ... }, ... ] }
""")
s.append(Paragraph("6.3 Consultar por ID: GET /productos/4", h2))
P("Devuelve el producto con ese id, o <b>404 Not Found</b> si no existe:")
code("""
{ "error": "No existe un producto con id 999" }
""")
s.append(Paragraph("6.4 Actualizar: PUT y PATCH /productos/4", h2))
P("<b>PUT</b> reemplaza el producto completo (los campos obligatorios deben venir); <b>PATCH</b> modifica solo "
  "los campos enviados, por ejemplo <font face='Courier'>{\"stock\": 50}</font>. Ambos devuelven el producto "
  "actualizado y renuevan <font face='Courier'>actualizado_en</font>.")
s.append(Paragraph("6.5 Eliminar: DELETE /productos/4", h2))
code("""
{ "mensaje": "Producto 4 eliminado correctamente" }
""")
s.append(Paragraph("6.6 Manejo de errores", h2))
P("Si los datos no son válidos, la API responde <b>400 Bad Request</b> e indica qué campo falló:")
code("""
{
  "error": "Datos inválidos",
  "detalles": {
    "categoria": "Campo obligatorio",
    "nombre": "Debe ser un texto no vacío",
    "precio": "Debe ser un número mayor o igual a 0"
  }
}
""")
tabla([["Código", "Significado en esta API"],
       ["200 OK", "Consulta, actualización o eliminación correcta"],
       ["201 Created", "Producto creado"],
       ["400 Bad Request", "JSON mal formado o datos que no cumplen las reglas"],
       ["404 Not Found", "El producto o la ruta no existen"],
       ["405 Method Not Allowed", "Método no soportado en esa ruta (por ejemplo, PUT /productos)"]],
      [4.4 * cm, ANCHO - 4.4 * cm])
P("Los códigos se eligieron según su definición en el estándar HTTP (Fielding et al., 2022; MDN Web Docs, s.f.).")

# ================================================================== 7. POSTMAN
s.append(PageBreak())
s.append(Paragraph("7. Pruebas en Postman", h1))
P("Las pruebas se ejecutaron en orden con la colección incluida en el proyecto. Cada petición tiene un script "
  "de prueba que confirma el código de respuesta esperado (Postman, s.f.).")
captura("01_crear", 1, "POST /productos: creación del producto, respuesta 201 Created.")
captura("02_listar", 2, "GET /productos: consulta de todos los productos.")
captura("03_por_id", 3, "GET /productos/{id}: consulta del producto creado.")
captura("04_put", 4, "PUT /productos/{id}: actualización de precio, stock y descripción.")
captura("05_patch", 5, "PATCH /productos/{id}: actualización solo del stock.")
captura("06_eliminar", 6, "DELETE /productos/{id}: eliminación del producto.")
captura("07_error_404", 7, "GET del producto eliminado: respuesta 404 Not Found.")
captura("08_error_400", 8, "POST con datos inválidos: respuesta 400 Bad Request con el detalle de errores.")

# ================================================================== 8. BD Y PYTEST
s.append(Paragraph("8. Verificación en la base de datos y pruebas automáticas", h1))
P("Para comprobar que los cambios realmente se guardan, se consultó la tabla directamente después de cada "
  "operación, con DB Browser for SQLite o desde la terminal:")
code("""
sqlite3 instance/inventario.db "SELECT id, nombre, precio, stock FROM productos;"
""")
captura("09_base_de_datos", 9, "Tabla productos en SQLite después de las operaciones CRUD.")
P("Además, el proyecto incluye 10 pruebas automáticas con pytest que cubren las cinco operaciones, los filtros "
  "y los casos de error (datos inválidos, JSON mal formado e id inexistente). Cada prueba usa una base de datos "
  "temporal, por lo que no altera los datos reales:")
code("""
python -m pytest -v
==================== 10 passed ====================
""")
captura("10_pytest", 10, "Resultado de las pruebas automáticas con pytest.")

# ================================================================== 9. CONCLUSIONES
s.append(Paragraph("9. Conclusiones", h1))
P("El proyecto cumple las cinco operaciones solicitadas (crear, consultar todos, consultar por ID, actualizar "
  "y eliminar) siguiendo los principios de REST: un recurso identificado por URL, métodos HTTP con su "
  "significado estándar y respuestas en JSON con códigos de estado adecuados.")
P("Más allá del CRUD, el trabajo me dejó tres aprendizajes. Primero, separar la aplicación en capas (rutas, "
  "validación y datos) hace que el código sea más fácil de explicar, probar y modificar. Segundo, validar la "
  "entrada y responder errores claros es tan importante como la funcionalidad, porque un cliente de la API "
  "necesita saber qué hizo mal. Tercero, combinar pruebas manuales en Postman con pruebas automáticas da "
  "confianza para hacer cambios sin romper lo que ya funcionaba.")
P("Como mejoras futuras se proponen la autenticación con tokens, la paginación de resultados, una tabla de "
  "movimientos de inventario (entradas y salidas) y el despliegue en un servidor en la nube.")

# ================================================================== REFERENCIAS
s.append(Paragraph("Referencias", h1))
for r in [
    "Fielding, R. T. (2000). <i>Architectural styles and the design of network-based software architectures</i> "
    "[Tesis doctoral, University of California, Irvine]. https://ics.uci.edu/~fielding/pubs/dissertation/top.htm",
    "Fielding, R., Nottingham, M., &amp; Reschke, J. (Eds.). (2022). <i>HTTP semantics</i> (RFC 9110). "
    "Internet Engineering Task Force. https://doi.org/10.17487/RFC9110",
    "Grinberg, M. (2018). <i>Flask web development: Developing web applications with Python</i> (2.ª ed.). O'Reilly Media.",
    "MDN Web Docs. (s.f.). <i>HTTP response status codes</i>. Mozilla. "
    "https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status",
    "Pallets. (2025). <i>Flask documentation</i> (versión 3.1.x). https://flask.palletsprojects.com/en/stable/",
    "Postman. (s.f.). <i>Postman docs</i>. https://learning.postman.com/docs/",
    "SQLite. (s.f.). <i>Appropriate uses for SQLite</i>. https://www.sqlite.org/whentouse.html",
]:
    s.append(Paragraph(r, ref))

doc = BaseDocTemplate(SALIDA, pagesize=letter, leftMargin=M, rightMargin=M,
                      topMargin=2.5 * cm, bottomMargin=2.5 * cm,
                      title="API REST de Inventario - Documentación",
                      author="Rodrigo Valdespino Vertiz")
frame = Frame(M, 2.5 * cm, ANCHO, H - 5 * cm, id="f")
doc.addPageTemplates([PageTemplate(id="portada", frames=[frame], onPage=portada),
                      PageTemplate(id="normal", frames=[frame], onPage=decor)])
doc.build(s)
print(f"PDF generado: {SALIDA}")
