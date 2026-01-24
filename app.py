import os
from flask import Flask, render_template, request, jsonify, Response
from groq import Groq

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/")
def index():
    # SOLUCIÓN TÉCNICA: Esto obliga a Chrome a cargar el diseño negro, no el texto plano
    return Response(render_template("dashboard.html"), mimetype='text/html')

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        mensaje = data.get("mensaje", "").lower()
        
        # IA DE CONSULTORÍA FORMAL (Llama 3.3 70B)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Eres una IA de consultoría de élite. Solo hablas de ciencia, medicina y finanzas con lenguaje formal técnico."},
                {"role": "user", "content": mensaje}
            ]
        )
        respuesta_texto = completion.choices[0].message.content

        # MOTOR DE IMÁGENES CORPORATIVAS (Solo Ciencia y Finanzas)
        if any(kw in mensaje for kw in ["imagen", "genera", "crea"]):
            filtro = "scientific visualization, medical data research, financial analysis charts, 8k, dark terminal, NO humans"
            url_imagen = f"https://pollinations.ai/p/{mensaje}_{filtro.replace(' ', '_')}?width=1080&height=720&seed=99"
            return jsonify({"respuesta": respuesta_texto, "imagen": url_imagen})

        return jsonify({"respuesta": respuesta_texto})
        
    except Exception as e:
        return jsonify({"respuesta": f"Error de Terminal: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)