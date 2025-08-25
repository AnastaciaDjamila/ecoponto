from flask import Flask, request, jsonify
from supabase import create_client, Client
from dotenv import load_dotenv
from bcrypt import hashpw, gensalt
import os

app = Flask(__name__)

# carregar variáveis de ambiente
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://kmdusyeonuuvljbkstye.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImttZHVzeWVvbnV1dmxqYmtzdHllIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTYxMzM0MjIsImV4cCI6MjA3MTcwOTQyMn0.sLoTCzJDUeqacLmMZb7XblDsUNoedxZFkhEw1K5NCEQ")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# rota para cadastrar moradores
@app.route("/cadastro", methods=["POST"])
def cadastro():
    data = request.json
    try:
        # criptografar a senha antes de salvar
        senha_hash = hashpw(data["senha"].encode("utf-8"), gensalt()).decode("utf-8")

        response = supabase.table("moradores").insert({
            "nome": data["nome"],
            "sexo": data.get("sexo"),
            "data_nascimento": data.get("data_nascimento"),  # formato: YYYY-MM-DD
            "email": data["email"],
            "telefone": data.get("telefone"),
            "endereco": data["endereco"],
            "senha": senha_hash

        }).execute()

        return jsonify({"message": "Morador cadastrado com sucesso!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# rota para listar moradores (sem mostrar senhas!)
@app.route("/moradores", methods=["GET"])
def listar():
    try:
        response = supabase.table("moradores").select("id, nome, email, telefone, endereco").execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
