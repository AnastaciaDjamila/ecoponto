import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://usuario:senha@host:5432/ecoponto_db")

commands = [
    """
    CREATE TABLE IF NOT EXISTS moradores (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    sexo VARCHAR(10), -- M/F/Outro
    data_nascimento DATE,
    telefone VARCHAR(20),
    endereco TEXT NOT NULL,
    senha VARCHAR(255) NOT NULL, -- Armazena senha (de preferência criptografada)
    data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    """,
    """
    CREATE TABLE IF NOT EXISTS pontos_recolha (
        id SERIAL PRIMARY KEY,
        nome VARCHAR(100) NOT NULL,
        endereco TEXT NOT NULL,
        bairro VARCHAR(100),
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS residuos (
        id SERIAL PRIMARY KEY,
        tipo VARCHAR(50) NOT NULL,
        descricao TEXT,
        peso_kg DECIMAL(10,2),
        id_morador INT REFERENCES moradores(id),
        id_ponto INT REFERENCES pontos_recolha(id),
        data_entrega TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS recompensas (
        id SERIAL PRIMARY KEY,
        nome VARCHAR(100) NOT NULL,
        pontos_necessarios INT NOT NULL,
        quantidade INT DEFAULT 0
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS trocas (
        id SERIAL PRIMARY KEY,
        id_morador INT REFERENCES moradores(id),
        id_recompensa INT REFERENCES recompensas(id),
        data_troca TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
]

def create_tables():
    try:
        con = psycopg2.connect(DATABASE_URL)
        cur = con.cursor()
        for command in commands:
            cur.execute(command)
        con.commit()
        cur.close()
        con.close()
        print("✅ Tabelas criadas com sucesso!")
    except Exception as e:
        print("❌ Erro ao criar tabelas:", e)

if __name__ == "__main__":
    create_tables()
