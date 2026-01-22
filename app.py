import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Esto lee la llave que pusiste en Render
api_key = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        mensaje = data.get("mensaje")
        # Genera la respuesta directamente
        response = model.generate_content(mensaje)
        return jsonify({"respuesta": response.text})
    except Exception as e:
        # Esto te dirá el error real en la consola de Render
        print(f"ERROR: {e}")
        return jsonify({"respuesta": "Error en el cerebro de IA."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))