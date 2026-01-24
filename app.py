import os
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)
# Configuración para billones: puerto dinámico para Render
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        mensaje = data.get("mensaje", "").lower()
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": mensaje}]
        )
        return jsonify({"respuesta": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"respuesta": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    # Render usa el puerto 10000 por defecto según tus logs
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)