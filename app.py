import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)

# Busca la llave que configuraste en el panel de Render
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        mensaje = data.get("mensaje")
        
        # Conexión con Llama 3 (Groq)
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": mensaje}]
        )
        
        # Aquí extraemos el texto de la respuesta correctamente
        respuesta_ia = completion.choices[0].message.content
        return jsonify({"respuesta": respuesta_ia})
        
    except Exception as e:
        print(f"Error detectado: {e}")
        return jsonify({"respuesta": "La IA no responde. Revisa si guardaste la llave en Render."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))