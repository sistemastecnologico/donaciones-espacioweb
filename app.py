import os
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/")
def index():
    # Carga el Dashboard Negro con Donaciones Crypto
    return render_template("dashboard.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        mensaje = data.get("mensaje", "").lower()
        
        # MOTOR DE IMÁGENES PROFESIONALES (Solo Ciencia/Finanzas)
        if any(keyword in mensaje for keyword in ["imagen", "genera", "crea", "visualiza"]):
            # Filtro de Élite: Bloqueo total de humanos, animales y morbo
            filtro_billonario = (
                "high-end scientific data visualization, financial market analysis charts, "
                "medical research graphics, abstract mathematical numbers, 8k resolution, "
                "dark mode aesthetic, NO humans, NO people, NO animals, NO organic life"
            )
            
            prompt_final = f"{mensaje} - {filtro_billonario}"
            url_imagen = f"https://pollinations.ai/p/{prompt_final.replace(' ', '_')}?width=1080&height=720&seed=77&model=flux"
            
            return jsonify({
                "respuesta": "Generando reporte visual de alta fidelidad para análisis corporativo...",
                "imagen": url_imagen
            })

        # IA DE CONSULTORÍA FORMAL
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "Eres una IA de consultoría para empresas billonarias. Solo hablas de ciencia, medicina, análisis y finanzas con lenguaje formal."},
                     {"role": "user", "content": mensaje}]
        )
        return jsonify({"respuesta": completion.choices[0].message.content})
        
    except Exception as e:
        return jsonify({"respuesta": f"Error en Terminal: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)