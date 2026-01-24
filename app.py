import os
from flask import Flask, request, jsonify, Response
from groq import Groq

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# EL MOTOR VISUAL NEGRO (Directo al navegador)
HTML_ULTIMATUM = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>TERMINAL BILLIONAIRE AI</title>
    <style>
        body { background-color: #000; color: #00ff00; font-family: 'Courier New', monospace; margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh; overflow: hidden; }
        .terminal { width: 80%; border: 2px solid #00ff00; background: #050505; padding: 40px; border-radius: 15px; box-shadow: 0 0 30px #004400; text-align: center; }
        .btn-donar { background: #f39c12; color: #000; padding: 12px 25px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; font-size: 1.1em; transition: 0.3s; margin-bottom: 20px; }
        .btn-donar:hover { background: #d35400; transform: scale(1.05); }
        #output { height: 200px; overflow-y: auto; text-align: left; border-bottom: 1px solid #333; margin-bottom: 20px; padding: 10px; color: #fff; }
        input { width: 90%; background: #111; border: 1px solid #00ff00; color: #00ff00; padding: 15px; font-size: 1.2em; outline: none; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="terminal">
        <button class="btn-donar">SISTEMA DE DONACIONES ACTIVO</button>
        <h1 style="margin: 10px 0;">SISTEMA IA DE ÉLITE</h1>
        <p style="color: #888;">Consultoría de alto nivel: Finanzas | Medicina | Ciencia</p>
        <div id="output">¡Conexión establecida! Esperando órdenes de consultoría...</div>
        <input type="text" placeholder="Ingrese consulta técnica de billonario..." onkeydown="if(event.key==='Enter') alert('Procesando con Llama 3.3 70B...')">
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    # FORZADO DE HTML: Esto elimina el error de "texto blanco" para siempre
    return Response(HTML_ULTIMATUM, mimetype='text/html')

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        mensaje = data.get("mensaje", "")
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "Eres un consultor de élite."}, {"role": "user", "content": mensaje}]
        )
        return jsonify({"respuesta": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"respuesta": f"Error de Sistema: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)