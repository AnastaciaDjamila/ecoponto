from flask import Flask, render_template, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Railway fornece a URL do banco como variável de ambiente
DATABASE_URL = os.getenv("DATABASE_URL")

# Página inicial (renderiza o index.html)
@app.route("/")
def home():
    return render_template("login-morador.html")

# Rota de login
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    telefone = data.get("telefone")
    senha = data.get("senha")

    if not telefone or not senha:
        return jsonify({"error": "Preencha todos os campos!"}), 400

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # Consulta básica (⚠️ ideal seria usar hash de senha)
        cur.execute("SELECT * FROM usuarios WHERE telefone=%s AND senha=%s", (telefone, senha))
        user = cur.fetchone()

        cur.close()
        conn.close()

        if user:
            return jsonify({"message": "✅ Login realizado com sucesso!"}), 200
        else:
            return jsonify({"error": "🚫 Telefone ou senha incorretos."}), 401

    except Exception as e:
        return jsonify({"error": f"Erro no servidor: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
