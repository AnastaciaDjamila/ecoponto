-- Usuários
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT
);

-- Recolhas
CREATE TABLE recolhas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    data DATE,
    hora TIME,
    material TEXT,
    pontos INTEGER,
    FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
);

-- Agendamentos
CREATE TABLE agendamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    data DATE,
    material TEXT,
    FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
);
