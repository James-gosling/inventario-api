CREATE TABLE IF NOT EXISTS productos (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre         TEXT    NOT NULL,
    categoria      TEXT    NOT NULL,
    precio         REAL    NOT NULL CHECK (precio >= 0),
    stock          INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0),
    descripcion    TEXT,
    creado_en      TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
    actualizado_en TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
);
