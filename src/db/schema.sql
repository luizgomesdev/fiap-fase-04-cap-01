-- Schema para banco de dados FarmTech Solutions
-- Tabela para armazenar medições dos sensores

CREATE TABLE medicoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts DATETIME DEFAULT CURRENT_TIMESTAMP,
    umidade REAL NOT NULL,
    ph REAL NOT NULL,
    p INTEGER NOT NULL,  -- Presença de fósforo (0/1)
    k INTEGER NOT NULL,  -- Presença de potássio (0/1)
    irrigou INTEGER NOT NULL  -- Status da irrigação (0/1)
);

-- Índices para melhorar performance de consultas
CREATE INDEX idx_timestamp ON medicoes(ts);
CREATE INDEX idx_umidade ON medicoes(umidade);
CREATE INDEX idx_irrigacao ON medicoes(irrigou);
